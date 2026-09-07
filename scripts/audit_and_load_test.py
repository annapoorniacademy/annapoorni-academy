"""
Master Production Audit & Load Testing Harness for Annapoorni Academy V2.0
Executes A-Z verification, security injection testing, endpoint inventory,
and multi-level concurrency/load testing (25, 50, 100, 150, 200 users).
"""

import sys
import os
import time
import json
import statistics
import threading
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import urllib.request
import urllib.error

BASE_URL = os.environ.get('TEST_BASE_URL', 'http://127.0.0.1:5000')

def make_request(method, endpoint, data=None, headers=None, timeout=10):
    url = f"{BASE_URL}{endpoint}"
    req_headers = headers.copy() if headers else {}
    req_data = None
    
    if data is not None:
        req_headers['Content-Type'] = 'application/json'
        req_data = json.dumps(data).encode('utf-8')
        
    req = urllib.request.Request(url, data=req_data, headers=req_headers, method=method)
    start_time = time.perf_counter()
    
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            latency = (time.perf_counter() - start_time) * 1000
            res_body = response.read().decode('utf-8')
            try:
                json_data = json.loads(res_body)
            except Exception:
                json_data = res_body
            return {
                'status_code': response.status,
                'latency': latency,
                'data': json_data,
                'error': None
            }
    except urllib.error.HTTPError as e:
        latency = (time.perf_counter() - start_time) * 1000
        try:
            err_body = e.read().decode('utf-8')
            json_err = json.loads(err_body)
        except Exception:
            json_err = str(e)
        return {
            'status_code': e.code,
            'latency': latency,
            'data': json_err,
            'error': str(e)
        }
    except Exception as e:
        latency = (time.perf_counter() - start_time) * 1000
        return {
            'status_code': 0,
            'latency': latency,
            'data': None,
            'error': str(e)
        }

# =============================================================================
# 1. API Endpoint Inventory & Edge-Case Audit
# =============================================================================

def run_endpoint_audit():
    print("\n=======================================================")
    print(" [RUNNING] API ROUTE INVENTORY & BOUNDARY AUDIT")
    print("=======================================================")
    
    results = []

    def log_test(name, passed, detail=""):
        status = "[PASS]" if passed else "[FAIL]"
        print(f"{status} {name} {f'- {detail}' if detail else ''}")
        results.append({'name': name, 'passed': passed, 'detail': detail})

    # 1. Health Endpoints
    h1 = make_request('GET', '/health')
    log_test("GET /health", h1['status_code'] == 200, f"Status: {h1['status_code']}")
    
    h2 = make_request('GET', '/api/health')
    log_test("GET /api/health", h2['status_code'] == 200, f"Status: {h2['status_code']}")

    # 2. SEO Endpoints
    rob = make_request('GET', '/robots.txt')
    log_test("GET /robots.txt", rob['status_code'] == 200 and "User-agent" in str(rob['data']))
    
    sm = make_request('GET', '/sitemap.xml')
    log_test("GET /sitemap.xml", sm['status_code'] == 200 and "urlset" in str(sm['data']))

    # 3. Public Content Endpoints
    s_set = make_request('GET', '/api/website/settings')
    log_test("GET /api/website/settings", s_set['status_code'] == 200)

    thm = make_request('GET', '/api/website/theme')
    log_test("GET /api/website/theme", thm['status_code'] == 200)

    hp = make_request('GET', '/api/homepage/sections')
    log_test("GET /api/homepage/sections", hp['status_code'] == 200)

    nav = make_request('GET', '/api/navigation')
    log_test("GET /api/navigation", nav['status_code'] == 200)

    soc = make_request('GET', '/api/social-links')
    log_test("GET /api/social-links", soc['status_code'] == 200)

    courses = make_request('GET', '/api/courses')
    log_test("GET /api/courses", courses['status_code'] == 200 and isinstance(courses['data'], list))

    c1 = make_request('GET', '/api/courses/1')
    log_test("GET /api/courses/1", c1['status_code'] == 200 and c1['data'].get('id') == 1)

    c_non = make_request('GET', '/api/courses/99999')
    log_test("GET /api/courses/99999 (Nonexistent)", c_non['status_code'] == 404)

    subjects = make_request('GET', '/api/subjects')
    log_test("GET /api/subjects", subjects['status_code'] == 200 and isinstance(subjects['data'], list))

    sub1 = make_request('GET', '/api/subjects/1')
    log_test("GET /api/subjects/1", sub1['status_code'] == 200)

    ann = make_request('GET', '/api/announcements')
    log_test("GET /api/announcements", ann['status_code'] == 200)

    contact_info = make_request('GET', '/api/contact')
    log_test("GET /api/contact", contact_info['status_code'] == 200)

    # 4. Contact Form Boundary & Security Tests
    c_valid = make_request('POST', '/api/contact/inquiry', {
        'name': 'Production Tester',
        'email': 'tester@example.com',
        'phone': '+91 90803 85589',
        'mode': 'Live Online via Zoom',
        'subject': 'Load Test Inquiry',
        'message': 'Testing message payload'
    })
    log_test("POST /api/contact/inquiry (Valid)", c_valid['status_code'] == 201 and 'inquiry' in c_valid['data'])

    c_missing = make_request('POST', '/api/contact/inquiry', {'name': 'Missing fields'})
    log_test("POST /api/contact/inquiry (Missing fields)", c_missing['status_code'] == 400)

    c_xss = make_request('POST', '/api/contact/inquiry', {
        'name': '<script>alert(1)</script>',
        'email': 'xss@example.com',
        'phone': '+91 90803 85589',
        'mode': 'Live Online',
        'subject': '<img src=x onerror=alert(1)>',
        'message': '<svg/onload=alert(1)>'
    })
    log_test("POST /api/contact/inquiry (XSS Payload)", c_xss['status_code'] == 201)

    c_sqli = make_request('POST', '/api/contact/inquiry', {
        'name': "' OR '1'='1' --",
        'email': "sqli@example.com",
        'phone': "'+91 90803 85589'",
        'mode': "Live Online",
        'subject': "'; DROP TABLE contact_inquiries; --",
        'message': "SQL injection probe"
    })
    log_test("POST /api/contact/inquiry (SQLi probe)", c_sqli['status_code'] == 201)

    c_oversized = make_request('POST', '/api/contact/inquiry', {
        'name': 'Long Message Tester',
        'email': 'long@example.com',
        'phone': '+91 90803 85589',
        'mode': 'Live Online',
        'subject': 'Large payload test',
        'message': 'A' * 5000
    })
    log_test("POST /api/contact/inquiry (Oversized payload 5KB)", c_oversized['status_code'] == 201)

    # 5. Course Enrollment Boundary & Security Tests
    enr_valid = make_request('POST', '/api/courses/1/enroll', {
        'student_name': 'Test Student Registration',
        'email': 'student.reg@example.com',
        'phone': '+91 90803 85589',
        'preferred_mode': 'Live Online via Zoom',
        'message': 'Ready to enroll'
    })
    log_test("POST /api/courses/1/enroll (Valid)", enr_valid['status_code'] == 201 and 'enrollment' in enr_valid['data'])

    enr_missing = make_request('POST', '/api/courses/1/enroll', {'student_name': 'Incomplete'})
    log_test("POST /api/courses/1/enroll (Missing fields)", enr_missing['status_code'] == 400)

    # 6. Admin Authentication & Protection
    admin_login = make_request('POST', '/api/admin/login', {'username': 'admin', 'password': '$12345678'})
    token = admin_login['data'].get('token') if admin_login['status_code'] == 200 else None
    log_test("POST /api/admin/login (Valid)", admin_login['status_code'] == 200 and bool(token))

    admin_invalid = make_request('POST', '/api/admin/login', {'username': 'admin', 'password': 'wrongpassword'})
    log_test("POST /api/admin/login (Invalid Password)", admin_invalid['status_code'] == 401)

    admin_empty = make_request('POST', '/api/admin/login', {'username': '', 'password': ''})
    log_test("POST /api/admin/login (Empty credentials)", admin_empty['status_code'] == 400 or admin_empty['status_code'] == 401)

    # Protected Endpoints without token
    unauth_dash = make_request('GET', '/api/admin/dashboard')
    log_test("GET /api/admin/dashboard (Unauthenticated)", unauth_dash['status_code'] == 401)

    unauth_enr = make_request('GET', '/api/admin/enrollments')
    log_test("GET /api/admin/enrollments (Unauthenticated)", unauth_enr['status_code'] == 401)

    unauth_inq = make_request('GET', '/api/admin/contact/inquiries')
    log_test("GET /api/admin/contact/inquiries (Unauthenticated)", unauth_inq['status_code'] == 401)

    unauth_bk = make_request('GET', '/api/admin/backup/export')
    log_test("GET /api/admin/backup/export (Unauthenticated)", unauth_bk['status_code'] == 401)

    # Protected Endpoints with valid token
    if token:
        auth_headers = {'Authorization': f'Bearer {token}'}
        auth_dash = make_request('GET', '/api/admin/dashboard', headers=auth_headers)
        log_test("GET /api/admin/dashboard (Authenticated)", auth_dash['status_code'] == 200 and 'metrics' in auth_dash['data'])

        auth_enr = make_request('GET', '/api/admin/enrollments', headers=auth_headers)
        log_test("GET /api/admin/enrollments (Authenticated)", auth_enr['status_code'] == 200 and isinstance(auth_enr['data'], list))

        auth_inq = make_request('GET', '/api/admin/contact/inquiries', headers=auth_headers)
        log_test("GET /api/admin/contact/inquiries (Authenticated)", auth_inq['status_code'] == 200 and isinstance(auth_inq['data'], list))

        auth_bk = make_request('GET', '/api/admin/backup/export', headers=auth_headers)
        log_test("GET /api/admin/backup/export (Authenticated)", auth_bk['status_code'] == 200 and auth_bk['data'].get('version') == '2.0.0')

    # Security check on response data
    all_responses_str = json.dumps([r['data'] for r in [c_valid, enr_valid, admin_login, s_set, contact_info]])
    leaks = [s for s in ['MAIL_PASSWORD', 'SECRET_KEY', 'JWT_SECRET_KEY', 'smtp_pass'] if s in all_responses_str]
    log_test("Secret leak scan across API responses", len(leaks) == 0, f"Leaks found: {leaks}")

    passed_count = sum(1 for r in results if r['passed'])
    print(f"\nInventory Audit Finished: {passed_count}/{len(results)} passed.")
    return results

# =============================================================================
# 2. Multi-Level Concurrency & Load Testing Harness
# =============================================================================

def user_journey_session(user_idx):
    """
    Simulates a realistic user journey:
    1. Check /health
    2. Read website settings & theme
    3. Read homepage sections
    4. Read courses list & subjects list
    5. Read course details
    6. Read announcements
    7. (10% of users) submit an inquiry or enrollment
    """
    latencies = []
    errors = 0
    http_5xx = 0
    http_4xx = 0

    endpoints_to_visit = [
        ('GET', '/health', None),
        ('GET', '/api/website/settings', None),
        ('GET', '/api/website/theme', None),
        ('GET', '/api/homepage/sections', None),
        ('GET', '/api/courses', None),
        ('GET', '/api/subjects', None),
        ('GET', '/api/courses/1', None),
        ('GET', '/api/announcements', None),
    ]

    # 10% of visitors submit an inquiry
    if user_idx % 10 == 0:
        endpoints_to_visit.append(('POST', '/api/contact/inquiry', {
            'name': f'Concurrent User {user_idx}',
            'email': f'user{user_idx}@loadtest.local',
            'phone': '+91 90803 85589',
            'mode': 'Live Online via Zoom',
            'subject': 'Concurrency Test Submission',
            'message': f'Automated load test session {user_idx}'
        }))

    for method, ep, payload in endpoints_to_visit:
        res = make_request(method, ep, payload, timeout=12)
        latencies.append(res['latency'])
        if res['status_code'] == 0 or res['error'] is not None:
            errors += 1
        elif res['status_code'] >= 500:
            http_5xx += 1
            errors += 1
        elif res['status_code'] >= 400:
            http_4xx += 1

    return {
        'requests': len(endpoints_to_visit),
        'errors': errors,
        'http_5xx': http_5xx,
        'http_4xx': http_4xx,
        'latencies': latencies
    }

def run_concurrency_level(concurrency_level, total_users):
    """Run load test with specified concurrency."""
    print(f"\n--- Testing Concurrency Level: {concurrency_level} simultaneous users ({total_users} user sessions) ---")
    start_time = time.perf_counter()
    
    all_latencies = []
    total_requests = 0
    total_errors = 0
    total_5xx = 0
    total_4xx = 0

    with ThreadPoolExecutor(max_workers=concurrency_level) as executor:
        futures = [executor.submit(user_journey_session, i) for i in range(total_users)]
        for future in as_completed(futures):
            try:
                res = future.result()
                total_requests += res['requests']
                total_errors += res['errors']
                total_5xx += res['http_5xx']
                total_4xx += res['http_4xx']
                all_latencies.extend(res['latencies'])
            except Exception as e:
                total_errors += 1

    total_duration = time.perf_counter() - start_time
    successful_requests = total_requests - total_errors
    success_pct = (successful_requests / total_requests * 100) if total_requests > 0 else 0
    five_xx_pct = (total_5xx / total_requests * 100) if total_requests > 0 else 0
    rps = total_requests / total_duration if total_duration > 0 else 0

    avg_lat = statistics.mean(all_latencies) if all_latencies else 0
    p50_lat = statistics.median(all_latencies) if all_latencies else 0
    all_latencies.sort()
    p95_lat = all_latencies[int(len(all_latencies) * 0.95)] if all_latencies else 0
    p99_lat = all_latencies[int(len(all_latencies) * 0.99)] if all_latencies else 0
    max_lat = max(all_latencies) if all_latencies else 0

    result_status = "PASS" if (success_pct >= 99.0 and five_xx_pct < 1.0) else ("DEGRADED" if success_pct >= 90.0 else "FAIL")

    print(f"Total Requests: {total_requests} | Success: {success_pct:.1f}% | 5xx: {five_xx_pct:.2f}%")
    print(f"RPS: {rps:.1f} req/s | Avg: {avg_lat:.1f}ms | p50: {p50_lat:.1f}ms | p95: {p95_lat:.1f}ms | p99: {p99_lat:.1f}ms | Max: {max_lat:.1f}ms")
    print(f"Result: {result_status}")

    return {
        'concurrency': concurrency_level,
        'total_requests': total_requests,
        'success_pct': f"{success_pct:.1f}%",
        'five_xx_pct': f"{five_xx_pct:.2f}%",
        'rps': f"{rps:.1f}",
        'avg': f"{avg_lat:.1f}ms",
        'p50': f"{p50_lat:.1f}ms",
        'p95': f"{p95_lat:.1f}ms",
        'p99': f"{p99_lat:.1f}ms",
        'max': f"{max_lat:.1f}ms",
        'status': result_status
    }

def main():
    print("================================================================================")
    print(" ANNAPOORNI ACADEMY V2.0 - MASTER AUDIT & CONCURRENCY / LOAD TEST HARNESS")
    print(f" Target Base URL: {BASE_URL}")
    print(f" Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("================================================================================")

    # 1. Run endpoint & boundary audit
    audit_results = run_endpoint_audit()

    # 2. Run multi-tier concurrency tests
    print("\n=======================================================")
    print(" [BENCHMARK] RUNNING MULTI-TIER LOAD / CONCURRENCY BENCHMARKS")
    print("=======================================================")
    
    levels = [
        (25, 50),     # Level 1: 25 concurrent users
        (50, 100),    # Level 2: 50 concurrent users
        (100, 200),   # Level 3: 100 concurrent users (Mandatory target)
        (150, 300),   # Level 4: 150 concurrent users
        (200, 400)    # Level 5: 200 concurrent users (Stress limit probe)
    ]

    load_results = []
    for conc, users in levels:
        res = run_concurrency_level(conc, users)
        load_results.append(res)
        time.sleep(1) # brief recovery interval between levels

    # 3. Print Summary Table
    print("\n========================================================================================")
    print(" [SUMMARY] MASTER CONCURRENCY TEST SUMMARY TABLE")
    print("========================================================================================")
    print(f"{'Users':<10} | {'Requests':<10} | {'Success %':<10} | {'5xx %':<8} | {'Avg Lat':<10} | {'p95 Lat':<10} | {'p99 Lat':<10} | {'Max Lat':<10} | {'Result':<8}")
    print("-" * 92)
    for r in load_results:
        print(f"{r['concurrency']:<10} | {r['total_requests']:<10} | {r['success_pct']:<10} | {r['five_xx_pct']:<8} | {r['avg']:<10} | {r['p95']:<10} | {r['p99']:<10} | {r['max']:<10} | {r['status']:<8}")
    print("========================================================================================")

    # 4. Save results to JSON artifact
    output_path = os.path.join(os.path.dirname(__file__), 'audit_and_load_results.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'audit': audit_results,
            'load': load_results
        }, f, indent=2)
    print(f"\nAudit and benchmark metrics written to: {output_path}")

if __name__ == '__main__':
    main()
