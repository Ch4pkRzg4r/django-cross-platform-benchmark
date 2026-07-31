import http from 'k6/http';
import { check, sleep } from 'k6';
import { Trend, Counter, Rate } from 'k6/metrics';

http.setResponseCallback(http.expectedStatuses({ min: 200, max: 399 }, 403));

const trendCart    = new Trend('latency_cart', true);
const trendShop    = new Trend('latency_shop', true);
const trendAbout   = new Trend('latency_about', true);
const counterErrors = new Counter('errors_total');
const rateOk        = new Rate('rate_ok');

const BASE_URL    = __ENV.BASE_URL    || 'http://20.218.108.186:8000';
const PLATFORM_ID = __ENV.PLATFORM_ID || 'unknown';
const REP         = __ENV.REP         || '0';
const TARGET_RPS  = parseInt(__ENV.TARGET_RPS || '10');
const DURATION    = __ENV.DURATION    || '30m';

export const options = {
  scenarios: {
    checkout: {
      executor: 'constant-arrival-rate',
      rate: TARGET_RPS,
      timeUnit: '1s',
      duration: DURATION,
      preAllocatedVUs: 20,
      maxVUs: 200,
      gracefulStop: '30s',
    },
  },
  thresholds: { 'http_req_failed': ['rate<0.20'] },
  tags: { platform: PLATFORM_ID, scenario: 'C_checkout', rep: REP },
  summaryTrendStats: ['avg', 'min', 'med', 'max', 'p(50)', 'p(90)', 'p(95)', 'p(99)', 'p(99.9)'],
  noConnectionReuse: false,
  insecureSkipTLSVerify: false,
  userAgent: 'k6-thesis-bench/1.0 (Phase7-Checkout; Sulaymaniyah; +chapk-thesis)',
};

export default function () {
  const r1 = http.get(BASE_URL + '/shop/', { tags: { endpoint: 'shop' }, timeout: '60s', redirects: 0 });
  trendShop.add(r1.timings.duration);
  let ok = (r1.status === 200);
  if (!ok) counterErrors.add(1);
  rateOk.add(ok);
  check(r1, { 'shop 200': () => ok });
  sleep(0.5);

  const r2 = http.get(BASE_URL + '/cart/', { tags: { endpoint: 'cart' }, timeout: '60s', redirects: 0 });
  trendCart.add(r2.timings.duration);
  ok = (r2.status === 200 || r2.status === 302);
  if (!ok) counterErrors.add(1);
  rateOk.add(ok);
  check(r2, { 'cart 200/302': () => ok });
  sleep(0.5);

  const r3 = http.get(BASE_URL + '/about/', { tags: { endpoint: 'about' }, timeout: '60s', redirects: 0 });
  trendAbout.add(r3.timings.duration);
  ok = (r3.status === 200);
  if (!ok) counterErrors.add(1);
  rateOk.add(ok);
  check(r3, { 'about 200': () => ok });
}

export function handleSummary(data) { return { 'stdout': '' }; }