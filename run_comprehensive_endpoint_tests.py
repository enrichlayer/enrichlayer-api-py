#!/usr/bin/env python3
"""
Run comprehensive endpoint tests and save results to files.
"""

import sys
import os
import subprocess
import time
import json
from datetime import datetime

def run_comprehensive_tests():
    """Run all endpoint tests and save results to files."""
    
    api_key = "a3c4354f-6f80-419a-8f8b-67d41d52c746"
    start_time = time.time()
    
    print("🧪 RUNNING COMPREHENSIVE ENDPOINT TESTS")
    print("=" * 60)
    print("Results will be saved to multiple output files...")
    print("=" * 60)
    
    # Set environment variable for tests
    os.environ['ENRICHLAYER_API_KEY'] = api_key
    
    all_results = []
    
    # Test 1: Core working tests (direct client)
    print("\n1️⃣ Testing Direct EnrichLayer Client...")
    direct_results = test_direct_client()
    all_results.extend(direct_results)
    
    # Test 2: Compatibility layer tests  
    print("\n2️⃣ Testing Proxycurl Compatibility Layer...")
    compat_results = test_compatibility_layer()
    all_results.extend(compat_results)
    
    # Test 3: Run core test suites
    print("\n3️⃣ Running Core Test Suites...")
    core_test_results = run_core_tests()
    
    # Generate comprehensive report
    total_duration = time.time() - start_time
    generate_comprehensive_report(all_results, core_test_results, total_duration)
    
    print(f"\n🎉 ALL TESTS COMPLETED!")
    print(f"📁 Check these output files:")
    print(f"   • endpoint_test_results_detailed.json")
    print(f"   • endpoint_test_summary.txt") 
    print(f"   • core_test_output.txt")
    print(f"   • comprehensive_test_report.json")


def test_direct_client():
    """Test direct EnrichLayer client endpoints."""
    from enrichlayer_client.gevent import EnrichLayer
    
    client = EnrichLayer(api_key=os.environ['ENRICHLAYER_API_KEY'])
    results = []
    
    test_urls = {
        "person": "https://www.linkedin.com/in/williamhgates/",
        "company": "https://www.linkedin.com/company/apple",
        "school": "https://www.linkedin.com/school/national-university-of-singapore/",
        "job": "https://www.linkedin.com/jobs/view/3586148395"
    }
    
    # Enhanced test cases with more endpoints
    test_cases = [
        # General
        ("get_balance", lambda: client.get_balance(), 0),
        
        # Person endpoints
        ("person.get", lambda: client.person.get(
            linkedin_profile_url=test_urls["person"], extra="exclude"
        ), 1),
        ("person.get_with_extra", lambda: client.person.get(
            linkedin_profile_url=test_urls["person"], extra="include"
        ), 2),
        ("person.search", lambda: client.person.search(
            country="US", first_name="John", last_name="Smith", enrich_profiles="skip"
        ), 10),
        ("person.resolve", lambda: client.person.resolve(
            company_domain="microsoft.com", first_name="Bill", last_name="Gates"
        ), 2),
        ("person.resolve_by_email", lambda: client.person.resolve_by_email(
            email="bill@microsoft.com", lookup_depth="deep"
        ), 1),
        ("person.resolve_by_phone", lambda: client.person.resolve_by_phone(
            phone_number="+1234567890"
        ), 1),
        ("person.lookup_email", lambda: client.person.lookup_email(
            linkedin_profile_url=test_urls["person"]
        ), 1),
        ("person.personal_contact", lambda: client.person.personal_contact(
            linkedin_profile_url=test_urls["person"]
        ), 1),
        ("person.personal_email", lambda: client.person.personal_email(
            linkedin_profile_url=test_urls["person"]
        ), 1),
        ("person.profile_picture", lambda: client.person.profile_picture(
            linkedin_person_profile_url=test_urls["person"]
        ), 0),
        
        # Company endpoints
        ("company.get", lambda: client.company.get(url=test_urls["company"]), 1),
        ("company.search", lambda: client.company.search(
            country="US", region="California", type="Public Company"
        ), 10),
        ("company.resolve", lambda: client.company.resolve(
            company_name="Apple", company_domain="apple.com"
        ), 2),
        ("company.find_job", lambda: client.company.find_job(
            keyword="engineer", geo_id="103644278"
        ), 2),
        ("company.job_count", lambda: client.company.job_count(
            keyword="engineer", geo_id="103644278"
        ), 1),
        ("company.employee_count", lambda: client.company.employee_count(
            url=test_urls["company"]
        ), 1),
        ("company.employee_list", lambda: client.company.employee_list(
            url=test_urls["company"]
        ), 1),
        ("company.employee_search", lambda: client.company.employee_search(
            keyword_regex="CEO", linkedin_company_profile_url=test_urls["company"]
        ), 3),
        ("company.role_lookup", lambda: client.company.role_lookup(
            company_name="apple", role="CEO"
        ), 3),
        ("company.profile_picture", lambda: client.company.profile_picture(
            linkedin_company_profile_url=test_urls["company"]
        ), 0),
        
        # School endpoints
        ("school.get", lambda: client.school.get(url=test_urls["school"]), 1),
        ("school.student_list", lambda: client.school.student_list(
            linkedin_school_url=test_urls["school"]
        ), 1),
        
        # Job endpoints
        ("job.get", lambda: client.job.get(url=test_urls["job"]), 1),
        
        # Customer endpoints
        ("customers.listing", lambda: client.customers.listing(), 1),
    ]
    
    # Add bulk operation test
    from enrichlayer_client.gevent import do_bulk
    bulk_test_cases = [
        ("do_bulk", lambda: do_bulk([
            (client.person.get, {"linkedin_profile_url": test_urls["person"]}),
            (client.company.get, {"url": test_urls["company"]}),
            (client.school.get, {"url": test_urls["school"]}),
        ]), 3),
    ]
    
    # Combine all test cases
    all_test_cases = test_cases + bulk_test_cases
    
    print("   Running direct client tests...")
    for endpoint_name, test_func, expected_credits in all_test_cases:
        test_start = time.time()
        try:
            print(f"   • {endpoint_name}...", end=" ")
            result = test_func()
            duration = time.time() - test_start
            
            # Extract sample data
            sample_data = extract_sample_data(endpoint_name, result)
            
            results.append({
                "endpoint": endpoint_name,
                "client_type": "direct",
                "status": "success",
                "duration": round(duration, 3),
                "credits_used": expected_credits,
                "sample_data": sample_data,
                "timestamp": datetime.now().isoformat()
            })
            print(f"✅ ({duration:.2f}s)")
            
        except Exception as e:
            duration = time.time() - test_start
            results.append({
                "endpoint": endpoint_name,
                "client_type": "direct",
                "status": "error",
                "duration": round(duration, 3),
                "credits_used": 0,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            })
            print(f"❌ ({str(e)[:50]}...)")
    
    return results


def test_compatibility_layer():
    """Test proxycurl compatibility layer."""
    # Enable compatibility
    from enrichlayer_client.compat import enable_proxycurl_compatibility
    enable_proxycurl_compatibility(api_key=os.environ['ENRICHLAYER_API_KEY'])
    
    from proxycurl.gevent import Proxycurl
    proxycurl = Proxycurl(api_key=os.environ['ENRICHLAYER_API_KEY'])
    
    results = []
    
    test_urls = {
        "person": "https://www.linkedin.com/in/williamhgates/",
        "company": "https://www.linkedin.com/company/apple", 
        "school": "https://www.linkedin.com/school/national-university-of-singapore/",
        "job": "https://www.linkedin.com/jobs/view/3586148395"
    }
    
    # Compatibility test cases - comprehensive coverage
    test_cases = [
        # General
        ("get_balance", lambda: proxycurl.get_balance(), 0),
        
        # Person endpoints
        ("linkedin.person.get", lambda: proxycurl.linkedin.person.get(
            linkedin_profile_url=test_urls["person"], extra="exclude"
        ), 1),
        ("linkedin.person.search", lambda: proxycurl.linkedin.person.search(
            country="US", first_name="John", last_name="Smith", enrich_profiles="skip"
        ), 10),
        ("linkedin.person.resolve", lambda: proxycurl.linkedin.person.resolve(
            company_domain="microsoft.com", first_name="Bill", last_name="Gates"
        ), 2),
        ("linkedin.person.resolve_by_email", lambda: proxycurl.linkedin.person.resolve_by_email(
            email="bill@microsoft.com", lookup_depth="deep"
        ), 1),
        ("linkedin.person.resolve_by_phone", lambda: proxycurl.linkedin.person.resolve_by_phone(
            phone_number="+1234567890"
        ), 1),
        ("linkedin.person.lookup_email", lambda: proxycurl.linkedin.person.lookup_email(
            linkedin_profile_url=test_urls["person"]
        ), 1),
        ("linkedin.person.personal_contact", lambda: proxycurl.linkedin.person.personal_contact(
            linkedin_profile_url=test_urls["person"]
        ), 1),
        ("linkedin.person.personal_email", lambda: proxycurl.linkedin.person.personal_email(
            linkedin_profile_url=test_urls["person"]
        ), 1),
        
        # Company endpoints
        ("linkedin.company.get", lambda: proxycurl.linkedin.company.get(
            url=test_urls["company"]
        ), 1),
        ("linkedin.company.search", lambda: proxycurl.linkedin.company.search(
            country="US", region="California", type="Public Company"
        ), 10),
        ("linkedin.company.resolve", lambda: proxycurl.linkedin.company.resolve(
            company_name="Apple", company_domain="apple.com"
        ), 2),
        ("linkedin.company.find_job", lambda: proxycurl.linkedin.company.find_job(
            keyword="engineer", geo_id="103644278"
        ), 2),
        ("linkedin.company.job_count", lambda: proxycurl.linkedin.company.job_count(
            keyword="engineer", geo_id="103644278"
        ), 1),
        ("linkedin.company.employee_count", lambda: proxycurl.linkedin.company.employee_count(
            url=test_urls["company"]
        ), 1),
        ("linkedin.company.employee_list", lambda: proxycurl.linkedin.company.employee_list(
            url=test_urls["company"]
        ), 1),
        ("linkedin.company.employee_search", lambda: proxycurl.linkedin.company.employee_search(
            keyword_regex="CEO", linkedin_company_profile_url=test_urls["company"]
        ), 3),
        ("linkedin.company.role_lookup", lambda: proxycurl.linkedin.company.role_lookup(
            company_name="apple", role="CEO"
        ), 3),
        
        # School endpoints
        ("linkedin.school.get", lambda: proxycurl.linkedin.school.get(
            url=test_urls["school"]
        ), 1),
        ("linkedin.school.student_list", lambda: proxycurl.linkedin.school.student_list(
            linkedin_school_url=test_urls["school"]
        ), 1),
        
        # Job endpoints
        ("linkedin.job.get", lambda: proxycurl.linkedin.job.get(
            url=test_urls["job"]
        ), 1),
        
        # Customer endpoints
        ("customers.listing", lambda: proxycurl.customers.listing(), 1),
    ]
    
    # Add bulk operation test for compatibility
    from enrichlayer_client.gevent import do_bulk
    bulk_test_cases = [
        ("do_bulk", lambda: do_bulk([
            (proxycurl.linkedin.person.get, {"linkedin_profile_url": test_urls["person"]}),
            (proxycurl.linkedin.company.get, {"url": test_urls["company"]}),
            (proxycurl.linkedin.school.get, {"url": test_urls["school"]}),
        ]), 3),
    ]
    
    # Combine all compatibility test cases
    all_test_cases = test_cases + bulk_test_cases
    
    print("   Running compatibility layer tests...")
    for endpoint_name, test_func, expected_credits in all_test_cases:
        test_start = time.time()
        try:
            print(f"   • {endpoint_name}...", end=" ")
            result = test_func()
            duration = time.time() - test_start
            
            # Extract sample data
            sample_data = extract_sample_data(endpoint_name, result)
            
            results.append({
                "endpoint": endpoint_name,
                "client_type": "compatibility",
                "status": "success",
                "duration": round(duration, 3),
                "credits_used": expected_credits,
                "sample_data": sample_data,
                "timestamp": datetime.now().isoformat()
            })
            print(f"✅ ({duration:.2f}s)")
            
        except Exception as e:
            duration = time.time() - test_start
            results.append({
                "endpoint": endpoint_name,
                "client_type": "compatibility",
                "status": "error",
                "duration": round(duration, 3),
                "credits_used": 0,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            })
            print(f"❌ ({str(e)[:50]}...)")
    
    return results


def extract_sample_data(endpoint_name, result):
    """Extract relevant sample data from API response."""
    sample_data = {}
    
    if isinstance(result, dict):
        if endpoint_name in ["get_balance"]:
            sample_data = {"credit_balance": result.get("credit_balance")}
        elif "person.get" in endpoint_name:
            sample_data = {
                "full_name": result.get("full_name"),
                "headline": result.get("headline", "")[:80] + "..." if result.get("headline") else None,
                "experience_count": len(result.get("experiences", [])),
                "education_count": len(result.get("education", [])),
                "has_extra_data": bool(result.get("extra"))
            }
        elif "company.get" in endpoint_name:
            sample_data = {
                "name": result.get("name"),
                "industry": result.get("industry"),
                "follower_count": result.get("follower_count"),
                "employee_count": result.get("company_size")
            }
        elif "school.get" in endpoint_name:
            sample_data = {
                "name": result.get("name"),
                "industry": result.get("industry"),
                "follower_count": result.get("follower_count")
            }
        elif "job.get" in endpoint_name:
            sample_data = {
                "linkedin_internal_id": result.get("linkedin_internal_id"),
                "job_title": result.get("job_title"),
                "company": result.get("company")
            }
        else:
            # Generic sample for other endpoints
            sample_data = {k: v for k, v in list(result.items())[:3]} if result else {}
    
    return sample_data


def run_core_tests():
    """Run the core test suites."""
    print("   Running core library tests...")
    
    test_results = {}
    
    # Run core tests
    try:
        result = subprocess.run([
            sys.executable, 'tests/test_enrichlayer.py'
        ], capture_output=True, text=True, timeout=60)
        
        test_results['test_enrichlayer'] = {
            'returncode': result.returncode,
            'stdout': result.stdout,
            'stderr': result.stderr,
            'success': result.returncode == 0
        }
        print(f"   • Core library tests: {'✅' if result.returncode == 0 else '❌'}")
        
    except Exception as e:
        test_results['test_enrichlayer'] = {
            'error': str(e),
            'success': False
        }
        print(f"   • Core library tests: ❌ ({e})")
    
    # Run exception mapping tests
    try:
        result = subprocess.run([
            sys.executable, 'tests/test_exception_mapping.py'
        ], capture_output=True, text=True, timeout=60)
        
        test_results['test_exception_mapping'] = {
            'returncode': result.returncode,
            'stdout': result.stdout,
            'stderr': result.stderr,
            'success': result.returncode == 0
        }
        print(f"   • Exception mapping tests: {'✅' if result.returncode == 0 else '❌'}")
        
    except Exception as e:
        test_results['test_exception_mapping'] = {
            'error': str(e),
            'success': False
        }
        print(f"   • Exception mapping tests: ❌ ({e})")
    
    return test_results


def generate_comprehensive_report(api_results, core_results, total_duration):
    """Generate comprehensive test reports."""
    
    # Calculate API test statistics
    total_api_tests = len(api_results)
    successful_api_tests = len([r for r in api_results if r["status"] == "success"])
    failed_api_tests = total_api_tests - successful_api_tests
    api_success_rate = (successful_api_tests / total_api_tests * 100) if total_api_tests > 0 else 0
    total_credits = sum(r.get("credits_used", 0) for r in api_results)
    
    # Categorize results
    by_client_type = {}
    by_category = {}
    
    for result in api_results:
        client_type = result["client_type"]
        endpoint = result["endpoint"]
        status = result["status"]
        
        # By client type
        if client_type not in by_client_type:
            by_client_type[client_type] = {"total": 0, "success": 0, "error": 0}
        by_client_type[client_type]["total"] += 1
        by_client_type[client_type][status] += 1
        
        # By category
        if "." in endpoint:
            category = endpoint.split(".")[0] if endpoint != "get_balance" else "general"
        else:
            category = "general"
        
        if category not in by_category:
            by_category[category] = {"total": 0, "success": 0, "error": 0}
        by_category[category]["total"] += 1
        by_category[category][status] += 1
    
    # Save detailed JSON report
    detailed_report = {
        "test_summary": {
            "timestamp": datetime.now().isoformat(),
            "test_type": "comprehensive_endpoint_testing_with_fixed_parameters",
            "total_api_tests": total_api_tests,
            "successful_api_tests": successful_api_tests,
            "failed_api_tests": failed_api_tests,
            "api_success_rate": f"{api_success_rate:.1f}%",
            "total_credits_used": total_credits,
            "total_duration": round(total_duration, 3),
            "average_response_time": round(
                sum(r["duration"] for r in api_results) / total_api_tests, 3
            ) if total_api_tests > 0 else 0
        },
        "by_client_type": by_client_type,
        "by_category": by_category,
        "api_test_results": api_results,
        "core_test_results": core_results
    }
    
    with open("endpoint_test_results_detailed.json", "w") as f:
        json.dump(detailed_report, f, indent=2)
    
    # Save human-readable summary
    with open("endpoint_test_summary.txt", "w") as f:
        f.write("COMPREHENSIVE ENDPOINT TEST RESULTS\n")
        f.write("=" * 70 + "\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 70 + "\n\n")
        
        f.write("📊 OVERALL SUMMARY\n")
        f.write("-" * 30 + "\n")
        f.write(f"Total API Tests: {total_api_tests}\n")
        f.write(f"Successful: {successful_api_tests}\n")
        f.write(f"Failed: {failed_api_tests}\n")
        f.write(f"Success Rate: {api_success_rate:.1f}%\n")
        f.write(f"Total Credits Used: {total_credits}\n")
        f.write(f"Total Duration: {total_duration:.2f}s\n")
        f.write(f"Average Response Time: {detailed_report['test_summary']['average_response_time']}s\n\n")
        
        f.write("📊 BY CLIENT TYPE\n")
        f.write("-" * 30 + "\n")
        for client_type, stats in by_client_type.items():
            f.write(f"{client_type.upper()}: {stats['success']}/{stats['total']} successful ({stats['success']/stats['total']*100:.1f}%)\n")
        f.write("\n")
        
        f.write("📊 BY CATEGORY\n")
        f.write("-" * 30 + "\n")
        for category, stats in by_category.items():
            f.write(f"{category.upper()}: {stats['success']}/{stats['total']} successful ({stats['success']/stats['total']*100:.1f}%)\n")
        f.write("\n")
        
        f.write("✅ SUCCESSFUL ENDPOINTS\n")
        f.write("-" * 30 + "\n")
        for result in api_results:
            if result["status"] == "success":
                f.write(f"  ✅ {result['endpoint']} ({result['client_type']}) - {result['credits_used']} credits, {result['duration']}s\n")
        f.write("\n")
        
        if failed_api_tests > 0:
            f.write("❌ FAILED ENDPOINTS\n")
            f.write("-" * 30 + "\n")
            for result in api_results:
                if result["status"] == "error":
                    f.write(f"  ❌ {result['endpoint']} ({result['client_type']}) - {result.get('error', 'Unknown error')}\n")
            f.write("\n")
        
        f.write("🧪 CORE TEST RESULTS\n")
        f.write("-" * 30 + "\n")
        for test_name, result in core_results.items():
            status = "✅ PASSED" if result.get('success', False) else "❌ FAILED"
            f.write(f"{status}: {test_name}\n")
    
    # Save core test output separately
    with open("core_test_output.txt", "w") as f:
        f.write("CORE TEST SUITE OUTPUT\n")
        f.write("=" * 50 + "\n\n")
        
        for test_name, result in core_results.items():
            f.write(f"TEST: {test_name}\n")
            f.write("-" * 30 + "\n")
            f.write(f"Success: {result.get('success', False)}\n")
            f.write(f"Return Code: {result.get('returncode', 'N/A')}\n")
            
            if 'stdout' in result:
                f.write("\nSTDOUT:\n")
                f.write(result['stdout'])
            
            if 'stderr' in result and result['stderr']:
                f.write("\nSTDERR:\n")
                f.write(result['stderr'])
            
            if 'error' in result:
                f.write(f"\nERROR: {result['error']}\n")
            
            f.write("\n" + "=" * 50 + "\n\n")
    
    # Save minimal comprehensive report
    comprehensive_summary = {
        "timestamp": datetime.now().isoformat(),
        "api_tests": {
            "total": total_api_tests,
            "successful": successful_api_tests,
            "success_rate": f"{api_success_rate:.1f}%",
            "credits_used": total_credits
        },
        "core_tests": {
            test_name: result.get('success', False) 
            for test_name, result in core_results.items()
        },
        "summary": {
            "all_api_tests_passed": failed_api_tests == 0,
            "all_core_tests_passed": all(result.get('success', False) for result in core_results.values()),
            "production_ready": failed_api_tests == 0 and all(result.get('success', False) for result in core_results.values())
        }
    }
    
    with open("comprehensive_test_report.json", "w") as f:
        json.dump(comprehensive_summary, f, indent=2)


if __name__ == "__main__":
    run_comprehensive_tests()