// ========================================================================
// Scenario A: Browse (read-heavy)
// Constant arrival rate 50 RPS for 30 minutes
// Open-loop, coordinated-omission-safe (per Gil Tene)
// ========================================================================
// Thesis: Benchmarking and Evaluation of Traditional Web Servers and Serverless
//         Architectures for an E-Commerce System
// Author: Chapk Rzgar Mohammed Abdalla
// ========================================================================

import http from 'k6/http';

// Treat 200, 302, 403 (CSRF block) as successful responses for http_req_failed metric
http.setResponseCallback(http.expectedStatuses({ min: 200, max: 399 }, 403));
import { check } from 'k6';
import { Trend, Counter, Rate } from 'k6/metrics';

// --- Custom metrics for per-endpoint analysis ---
const trendShop      = new Trend('latency_shop',           true);
const trendHome      = new Trend('latency_home',           true);
const trendProduct   = new Trend('latency_product_detail', true);
const trendAbout     = new Trend('latency_about',          true);
const trendAdmin     = new Trend('latency_admin',          true);
const counterErrors  = new Counter('errors_total');
const rateOk         = new Rate('rate_ok');

// --- Environment variables passed by orchestrator ---
const BASE_URL    = __ENV.BASE_URL    || 'http://20.218.108.186:8000';
const TARGET_RPS  = parseInt(__ENV.TARGET_RPS  || '20');
const DURATION    = __ENV.DURATION    || '30m';
const PLATFORM_ID = __ENV.PLATFORM_ID || 'unknown';
const REP         = __ENV.REP         || '0';

// Pre-allocated VUs scale with target RPS:
// Rule of thumb: latency 250 ms * RPS = ~ concurrent VUs needed (Little's Law)
// Add 4x safety margin
const PRE_VUS = Math.max(20, TARGET_RPS * 2);
const MAX_VUS = Math.max(50, TARGET_RPS * 5);

export const options = {
  scenarios: {
    browse: {
      executor: 'constant-arrival-rate',
      rate: TARGET_RPS,
      timeUnit: '1s',
      duration: DURATION,
      preAllocatedVUs: PRE_VUS,
      maxVUs: MAX_VUS,
      gracefulStop: '30s',
    },
  },
  // Thresholds = "soft" SLOs for early warning, NOT for fail/pass academic decisions
  thresholds: {
    'http_req_failed':    ['rate<0.20'],     // <5% errors expected; if >5%, platform is overloaded
    // p99 < 10s (sanity check; cold starts spike)
  },
  // Tag metrics with platform + replication for downstream slicing
  tags: {
    platform:   PLATFORM_ID,
    scenario:   'A_browse',
    rep:        REP,
  },
  // Disable summary noise; orchestrator parses JSON streaming output
  summaryTrendStats: ['avg', 'min', 'med', 'max', 'p(50)', 'p(90)', 'p(95)', 'p(99)', 'p(99.9)'],
  // HTTP behavior tuning
  noConnectionReuse: false,    // Keep-alive: realistic browser behavior
  insecureSkipTLSVerify: false, // Verify TLS (Koyeb, ACA, Fly use real certs)
  userAgent: 'k6-thesis-bench/1.0 (Phase7-Browse; Sulaymaniyah; +chapk-thesis)',
};

// Weighted endpoint selection ( shop 40% / home 20% / product 20% / about 10% / admin 10% )
function pickEndpoint() {
  const r = Math.random();
  if (r < 0.40) return { path: '/shop/',           name: 'shop',    trend: trendShop };
  if (r < 0.60) return { path: '/',                name: 'home',    trend: trendHome };
  if (r < 0.80) return { path: '/product/1/', name: 'product', trend: trendProduct };
  if (r < 0.90) return { path: '/about/',          name: 'about',   trend: trendAbout };
                return { path: '/admin/login/',    name: 'admin',   trend: trendAdmin };
}

export default function () {
  const ep = pickEndpoint();
  const url = BASE_URL + ep.path;

  // Use http.get with explicit tag for per-endpoint metric attribution
  const res = http.get(url, {
    tags: { endpoint: ep.name },
    timeout: '60s',
    redirects: 0,  // Don't follow redirects; capture true server response time
  });

  // Per-endpoint latency tracking
  ep.trend.add(res.timings.duration);

  // Determine expected status code per endpoint
  // / redirects to /shop/ (302), all others should be 200
  const expectedOk = ep.name === 'home' ? (res.status === 302) : (res.status === 200);

  // Count errors
  if (!expectedOk) {
    counterErrors.add(1);
  }
  rateOk.add(expectedOk);

  // Per-iteration check (k6 native validation)
  check(res, {
    'status is expected':  () => expectedOk,
    'body has content':    (r) => r.body && r.body.length > 0,
    'duration < 30s':      (r) => r.timings.duration < 30000,
  });
}

// Hook called once at the end of the test
export function handleSummary(data) {
  // Orchestrator parses the JSON streaming output instead
  return {
    'stdout': '',
  };
}
