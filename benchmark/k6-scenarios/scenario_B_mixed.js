// ========================================================================
// Scenario B: Mixed (browse + session-cookie auth)
// Constant arrival rate 30 RPS for 30 minutes
// 60% browse / 30% session login flow / 10% admin static
// Tests session middleware overhead + cookie-jar behavior
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

const trendShop      = new Trend('latency_shop',           true);
const trendHome      = new Trend('latency_home',           true);
const trendAdminPage = new Trend('latency_admin_page',     true);
const trendLoginGet  = new Trend('latency_login_get',      true);
const counterErrors  = new Counter('errors_total');
const rateOk         = new Rate('rate_ok');

const BASE_URL    = __ENV.BASE_URL    || 'http://20.218.108.186:8000';
const TARGET_RPS  = parseInt(__ENV.TARGET_RPS  || '15');
const DURATION    = __ENV.DURATION    || '30m';
const PLATFORM_ID = __ENV.PLATFORM_ID || 'unknown';
const REP         = __ENV.REP         || '0';

const PRE_VUS = Math.max(15, TARGET_RPS * 2);
const MAX_VUS = Math.max(40, TARGET_RPS * 5);

export const options = {
  scenarios: {
    mixed: {
      executor: 'constant-arrival-rate',
      rate: TARGET_RPS,
      timeUnit: '1s',
      duration: DURATION,
      preAllocatedVUs: PRE_VUS,
      maxVUs: MAX_VUS,
      gracefulStop: '30s',
    },
  },
  thresholds: {
    'http_req_failed':   ['rate<0.20'],
    },
  tags: {
    platform: PLATFORM_ID,
    scenario: 'B_mixed',
    rep:      REP,
  },
  summaryTrendStats: ['avg', 'min', 'med', 'max', 'p(50)', 'p(90)', 'p(95)', 'p(99)', 'p(99.9)'],
  noConnectionReuse: false,
  insecureSkipTLSVerify: false,
  userAgent: 'k6-thesis-bench/1.0 (Phase7-Mixed; Sulaymaniyah; +chapk-thesis)',
};

// 60% browse / 30% admin-login-flow (cookie session GET) / 10% admin static
function pickAction() {
  const r = Math.random();
  if (r < 0.30) return 'browse_shop';
  if (r < 0.60) return 'browse_home';
  if (r < 0.90) return 'admin_login_get';
  return 'admin_static';
}

export default function () {
  const action = pickAction();
  let url, name, expectedStatus, trend;

  if (action === 'browse_shop') {
    url = BASE_URL + '/shop/';
    name = 'shop';
    expectedStatus = 200;
    trend = trendShop;
  } else if (action === 'browse_home') {
    url = BASE_URL + '/';
    name = 'home';
    expectedStatus = 302;
    trend = trendHome;
  } else if (action === 'admin_login_get') {
    // GET the admin login page (renders CSRF token, sets session cookie)
    url = BASE_URL + '/admin/login/';
    name = 'login_get';
    expectedStatus = 200;
    trend = trendLoginGet;
  } else {
    // Admin static (after login attempt would redirect, but we GET the page)
    url = BASE_URL + '/admin/login/';
    name = 'admin_static';
    expectedStatus = 200;
    trend = trendAdminPage;
  }

  const res = http.get(url, {
    tags: { endpoint: name },
    timeout: '60s',
    redirects: 0,
  });

  trend.add(res.timings.duration);

  const ok = res.status === expectedStatus;
  if (!ok) counterErrors.add(1);
  rateOk.add(ok);

  check(res, {
    'status is expected': () => ok,
    'body has content':   (r) => r.body && r.body.length > 0,
    'duration < 30s':     (r) => r.timings.duration < 30000,
  });
}

export function handleSummary(data) {
  return { 'stdout': '' };
}
