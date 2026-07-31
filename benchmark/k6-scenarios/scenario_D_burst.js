// ========================================================================
// Scenario D: Burst (sudden spike - Flash Sale pattern)
// Stages scale proportionally with DURATION env variable
//   At 30m: 5min baseline / 1min ramp up / 10min peak / 1min ramp down / 13min recovery
//   At  5m: 50s baseline /10s ramp up /100s peak /10s ramp down /130s recovery
// ========================================================================

import http from 'k6/http';

// Treat 200, 302, 403 (CSRF block) as successful responses for http_req_failed metric
http.setResponseCallback(http.expectedStatuses({ min: 200, max: 399 }, 403));
import { check } from 'k6';
import { Trend, Counter, Rate } from 'k6/metrics';

const trendShop     = new Trend('latency_shop', true);
const counterErrors = new Counter('errors_total');
const rateOk        = new Rate('rate_ok');

const BASE_URL    = __ENV.BASE_URL    || 'http://20.218.108.186:8000';
const PLATFORM_ID = __ENV.PLATFORM_ID || 'unknown';
const REP         = __ENV.REP         || '0';
const BASELINE_RPS = parseInt(__ENV.BASELINE_RPS || '5');
const PEAK_RPS     = parseInt(__ENV.PEAK_RPS     || '40');
const DURATION_MIN = parseInt(__ENV.DURATION_MIN || '30');

// Scale stages proportionally to DURATION_MIN
// 30min => [5, 1, 10, 1, 13]    sums to 30
// 10min => [1.67, 0.33, 3.33, 0.33, 4.33]  scale by 10/30
// 5min  => [0.83, 0.17, 1.67, 0.17, 2.17]
function s(min) { return Math.max(1, Math.round(min * 60)) + 's'; }
const SCALE = DURATION_MIN / 30.0;

export const options = {
  scenarios: {
    burst: {
      executor: 'ramping-arrival-rate',
      startRate: BASELINE_RPS,
      timeUnit: '1s',
      preAllocatedVUs: 30,
      maxVUs: 300,
      gracefulStop: '30s',
      stages: [
        { duration: s(5  * SCALE), target: BASELINE_RPS },  // baseline
        { duration: s(1  * SCALE), target: PEAK_RPS     },  // ramp UP
        { duration: s(10 * SCALE), target: PEAK_RPS     },  // peak
        { duration: s(1  * SCALE), target: BASELINE_RPS },  // ramp DOWN
        { duration: s(13 * SCALE), target: BASELINE_RPS },  // recovery
      ],
    },
  },
  thresholds: {
    'http_req_failed':   ['rate<0.20'],
  },
  tags: {
    platform: PLATFORM_ID,
    scenario: 'D_burst',
    rep:      REP,
  },
  summaryTrendStats: ['avg', 'min', 'med', 'max', 'p(50)', 'p(90)', 'p(95)', 'p(99)', 'p(99.9)'],
  noConnectionReuse: false,
  insecureSkipTLSVerify: false,
  userAgent: 'k6-thesis-bench/1.0 (Phase7-Burst; Sulaymaniyah; +chapk-thesis)',
};

export default function () {
  const res = http.get(BASE_URL + '/shop/', {
    tags: { endpoint: 'shop' },
    timeout: '60s',
    redirects: 0,
  });
  trendShop.add(res.timings.duration);
  const ok = res.status === 200;
  if (!ok) counterErrors.add(1);
  rateOk.add(ok);
  check(res, { 'shop status 200': () => ok });
}

export function handleSummary(data) {
  return { 'stdout': '' };
}