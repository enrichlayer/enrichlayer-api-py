#!/usr/bin/env python3
"""
Complete endpoint testing for ALL enrichlayer_client endpoints.

This script tests every available endpoint systematically based on the 
actual API structure found in the codebase.
"""

import asyncio
import json
import time
from datetime import datetime
from typing import Dict, Any, List

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from enrichlayer_client.asyncio import EnrichLayer


class CompleteEndpointTester:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.enrichlayer = EnrichLayer(api_key=api_key)
        self.results = []
        
    async def test_get_balance(self):
        """Test credit balance endpoint"""
        try:
            start_time = time.time()
            result = await self.enrichlayer.get_balance()
            end_time = time.time()
            
            self.results.append({
                "endpoint": "get_balance",
                "status": "success",
                "response_time": round(end_time - start_time, 3),
                "credits_used": 0,
                "sample_data": result
            })
        except Exception as e:
            self.results.append({
                "endpoint": "get_balance",
                "status": "error",
                "error": str(e)
            })

    # PERSON ENDPOINTS
    async def test_person_get(self):
        """Test person.get endpoint"""
        test_url = "https://www.linkedin.com/in/williamhgates/"
        try:
            start_time = time.time()
            result = await self.enrichlayer.person.get(linkedin_profile_url=test_url)
            end_time = time.time()
            
            self.results.append({
                "endpoint": "person.get",
                "status": "success",
                "response_time": round(end_time - start_time, 3),
                "credits_used": 1,
                "test_url": test_url,
                "sample_fields": {
                    "full_name": result.get("full_name", ""),
                    "headline": result.get("headline", "")[:100] if result.get("headline") else None,
                    "experience_count": len(result.get("experiences", [])),
                    "education_count": len(result.get("education", []))
                }
            })
        except Exception as e:
            self.results.append({
                "endpoint": "person.get",
                "status": "error",
                "error": str(e),
                "test_url": test_url
            })

    async def test_person_search(self):
        """Test person.search endpoint"""
        try:
            start_time = time.time()
            result = await self.enrichlayer.person.search(
                country="US",
                first_name="John",
                last_name="Smith"
            )
            end_time = time.time()
            
            self.results.append({
                "endpoint": "person.search",
                "status": "success",
                "response_time": round(end_time - start_time, 3),
                "credits_used": 10,  # Estimated
                "parameters": {"country": "US", "first_name": "John", "last_name": "Smith"},
                "sample_fields": {
                    "total_results": result.get("total_result_count", 0),
                    "results_count": len(result.get("results", [])),
                    "has_next_page": bool(result.get("next_page"))
                }
            })
        except Exception as e:
            self.results.append({
                "endpoint": "person.search",
                "status": "error",
                "error": str(e)
            })

    async def test_person_resolve(self):
        """Test person.resolve endpoint"""
        try:
            start_time = time.time()
            result = await self.enrichlayer.person.resolve(
                first_name="Bill",
                last_name="Gates",
                company_domain="microsoft.com"
            )
            end_time = time.time()
            
            self.results.append({
                "endpoint": "person.resolve",
                "status": "success",
                "response_time": round(end_time - start_time, 3),
                "credits_used": 2,
                "sample_fields": {
                    "found_url": result.get("url", ""),
                    "name_similarity": result.get("name_similarity_score", 0.0)
                }
            })
        except Exception as e:
            self.results.append({
                "endpoint": "person.resolve",
                "status": "error",
                "error": str(e)
            })

    async def test_person_resolve_by_email(self):
        """Test person.resolve_by_email endpoint"""
        try:
            start_time = time.time()
            result = await self.enrichlayer.person.resolve_by_email(
                email="bill@microsoft.com",
                lookup_depth="deep"
            )
            end_time = time.time()
            
            self.results.append({
                "endpoint": "person.resolve_by_email",
                "status": "success",
                "response_time": round(end_time - start_time, 3),
                "credits_used": 1,
                "sample_data": {k: v for k, v in result.items() if k not in ["profile"]}
            })
        except Exception as e:
            self.results.append({
                "endpoint": "person.resolve_by_email",
                "status": "error",
                "error": str(e)
            })

    async def test_person_resolve_by_phone(self):
        """Test person.resolve_by_phone endpoint"""
        try:
            start_time = time.time()
            result = await self.enrichlayer.person.resolve_by_phone(
                phone_number="+1234567890"
            )
            end_time = time.time()
            
            self.results.append({
                "endpoint": "person.resolve_by_phone",
                "status": "success",
                "response_time": round(end_time - start_time, 3),
                "credits_used": 1,
                "sample_data": result
            })
        except Exception as e:
            self.results.append({
                "endpoint": "person.resolve_by_phone",
                "status": "error",
                "error": str(e)
            })

    async def test_person_lookup_email(self):
        """Test person.lookup_email endpoint"""
        try:
            start_time = time.time()
            result = await self.enrichlayer.person.lookup_email(
                linkedin_profile_url="https://www.linkedin.com/in/williamhgates/"
            )
            end_time = time.time()
            
            self.results.append({
                "endpoint": "person.lookup_email",
                "status": "success",
                "response_time": round(end_time - start_time, 3),
                "credits_used": 1,
                "sample_data": result
            })
        except Exception as e:
            self.results.append({
                "endpoint": "person.lookup_email",
                "status": "error",
                "error": str(e)
            })

    async def test_person_personal_contact(self):
        """Test person.personal_contact endpoint"""
        try:
            start_time = time.time()
            result = await self.enrichlayer.person.personal_contact(
                linkedin_profile_url="https://www.linkedin.com/in/williamhgates/"
            )
            end_time = time.time()
            
            self.results.append({
                "endpoint": "person.personal_contact",
                "status": "success",
                "response_time": round(end_time - start_time, 3),
                "credits_used": 1,
                "sample_data": result
            })
        except Exception as e:
            self.results.append({
                "endpoint": "person.personal_contact",
                "status": "error",
                "error": str(e)
            })

    async def test_person_personal_email(self):
        """Test person.personal_email endpoint"""
        try:
            start_time = time.time()
            result = await self.enrichlayer.person.personal_email(
                linkedin_profile_url="https://www.linkedin.com/in/williamhgates/"
            )
            end_time = time.time()
            
            self.results.append({
                "endpoint": "person.personal_email",
                "status": "success",
                "response_time": round(end_time - start_time, 3),
                "credits_used": 1,
                "sample_data": result
            })
        except Exception as e:
            self.results.append({
                "endpoint": "person.personal_email",
                "status": "error",
                "error": str(e)
            })

    async def test_person_profile_picture(self):
        """Test person.profile_picture endpoint"""
        try:
            start_time = time.time()
            result = await self.enrichlayer.person.profile_picture(
                linkedin_person_profile_url="https://www.linkedin.com/in/williamhgates/"
            )
            end_time = time.time()
            
            self.results.append({
                "endpoint": "person.profile_picture",
                "status": "success",
                "response_time": round(end_time - start_time, 3),
                "credits_used": 0,
                "sample_data": result
            })
        except Exception as e:
            self.results.append({
                "endpoint": "person.profile_picture",
                "status": "error",
                "error": str(e)
            })

    # COMPANY ENDPOINTS
    async def test_company_get(self):
        """Test company.get endpoint"""
        test_url = "https://www.linkedin.com/company/apple/"
        try:
            start_time = time.time()
            result = await self.enrichlayer.company.get(url=test_url)
            end_time = time.time()
            
            self.results.append({
                "endpoint": "company.get",
                "status": "success",
                "response_time": round(end_time - start_time, 3),
                "credits_used": 1,
                "sample_fields": {
                    "name": result.get("name", ""),
                    "industry": result.get("industry", ""),
                    "follower_count": result.get("follower_count", 0)
                }
            })
        except Exception as e:
            self.results.append({
                "endpoint": "company.get",
                "status": "error",
                "error": str(e)
            })

    async def test_company_search(self):
        """Test company.search endpoint"""
        try:
            start_time = time.time()
            result = await self.enrichlayer.company.search(
                country="US",
                name="Apple"
            )
            end_time = time.time()
            
            self.results.append({
                "endpoint": "company.search",
                "status": "success",
                "response_time": round(end_time - start_time, 3),
                "credits_used": 10,  # Estimated
                "sample_fields": {
                    "total_results": result.get("total_result_count", 0),
                    "results_count": len(result.get("results", []))
                }
            })
        except Exception as e:
            self.results.append({
                "endpoint": "company.search",
                "status": "error",
                "error": str(e)
            })

    async def test_company_resolve(self):
        """Test company.resolve endpoint"""
        try:
            start_time = time.time()
            result = await self.enrichlayer.company.resolve(
                company_name="Apple",
                company_domain="apple.com"
            )
            end_time = time.time()
            
            self.results.append({
                "endpoint": "company.resolve",
                "status": "success",
                "response_time": round(end_time - start_time, 3),
                "credits_used": 2,
                "sample_data": {k: v for k, v in result.items() if k not in ["profile"]}
            })
        except Exception as e:
            self.results.append({
                "endpoint": "company.resolve",
                "status": "error",
                "error": str(e)
            })

    async def test_company_find_job(self):
        """Test company.find_job endpoint"""
        try:
            start_time = time.time()
            result = await self.enrichlayer.company.find_job(
                keyword="Apple"
            )
            end_time = time.time()
            
            self.results.append({
                "endpoint": "company.find_job",
                "status": "success",
                "response_time": round(end_time - start_time, 3),
                "credits_used": 2,
                "sample_fields": {
                    "job_count": len(result.get("job", [])) if result.get("job") else 0
                }
            })
        except Exception as e:
            self.results.append({
                "endpoint": "company.find_job",
                "status": "error",
                "error": str(e)
            })

    async def test_company_job_count(self):
        """Test company.job_count endpoint"""
        try:
            start_time = time.time()
            result = await self.enrichlayer.company.job_count(
                keyword="Apple"
            )
            end_time = time.time()
            
            self.results.append({
                "endpoint": "company.job_count",
                "status": "success",
                "response_time": round(end_time - start_time, 3),
                "credits_used": 1,
                "sample_data": result
            })
        except Exception as e:
            self.results.append({
                "endpoint": "company.job_count",
                "status": "error",
                "error": str(e)
            })

    async def test_company_employee_count(self):
        """Test company.employee_count endpoint"""
        try:
            start_time = time.time()
            result = await self.enrichlayer.company.employee_count(
                url="https://www.linkedin.com/company/apple/"
            )
            end_time = time.time()
            
            self.results.append({
                "endpoint": "company.employee_count",
                "status": "success",
                "response_time": round(end_time - start_time, 3),
                "credits_used": 1,
                "sample_data": result
            })
        except Exception as e:
            self.results.append({
                "endpoint": "company.employee_count",
                "status": "error",
                "error": str(e)
            })

    async def test_company_employee_list(self):
        """Test company.employee_list endpoint"""
        try:
            start_time = time.time()
            result = await self.enrichlayer.company.employee_list(
                url="https://www.linkedin.com/company/apple/"
            )
            end_time = time.time()
            
            self.results.append({
                "endpoint": "company.employee_list",
                "status": "success",
                "response_time": round(end_time - start_time, 3),
                "credits_used": 1,
                "sample_fields": {
                    "employee_count": len(result.get("employees", [])),
                    "has_next_page": bool(result.get("next_page"))
                }
            })
        except Exception as e:
            self.results.append({
                "endpoint": "company.employee_list",
                "status": "error",
                "error": str(e)
            })

    async def test_company_employee_search(self):
        """Test company.employee_search endpoint"""
        try:
            start_time = time.time()
            result = await self.enrichlayer.company.employee_search(
                linkedin_company_profile_url="https://www.linkedin.com/company/apple/",
                keyword_regex="engineer"
            )
            end_time = time.time()
            
            self.results.append({
                "endpoint": "company.employee_search",
                "status": "success",
                "response_time": round(end_time - start_time, 3),
                "credits_used": 3,
                "sample_fields": {
                    "employee_count": len(result.get("employees", [])),
                    "has_next_page": bool(result.get("next_page"))
                }
            })
        except Exception as e:
            self.results.append({
                "endpoint": "company.employee_search",
                "status": "error",
                "error": str(e)
            })

    async def test_company_role_lookup(self):
        """Test company.role_lookup endpoint"""
        try:
            start_time = time.time()
            result = await self.enrichlayer.company.role_lookup(
                role="CEO",
                company_name="Apple"
            )
            end_time = time.time()
            
            self.results.append({
                "endpoint": "company.role_lookup",
                "status": "success",
                "response_time": round(end_time - start_time, 3),
                "credits_used": 3,
                "sample_data": {k: v for k, v in result.items() if k not in ["profile"]}
            })
        except Exception as e:
            self.results.append({
                "endpoint": "company.role_lookup",
                "status": "error",
                "error": str(e)
            })

    async def test_company_profile_picture(self):
        """Test company.profile_picture endpoint"""
        try:
            start_time = time.time()
            result = await self.enrichlayer.company.profile_picture(
                linkedin_company_profile_url="https://www.linkedin.com/company/apple/"
            )
            end_time = time.time()
            
            self.results.append({
                "endpoint": "company.profile_picture",
                "status": "success",
                "response_time": round(end_time - start_time, 3),
                "credits_used": 0,
                "sample_data": result
            })
        except Exception as e:
            self.results.append({
                "endpoint": "company.profile_picture",
                "status": "error",
                "error": str(e)
            })

    # SCHOOL ENDPOINTS
    async def test_school_get(self):
        """Test school.get endpoint"""
        try:
            start_time = time.time()
            result = await self.enrichlayer.school.get(
                url="https://www.linkedin.com/school/national-university-of-singapore"
            )
            end_time = time.time()
            
            self.results.append({
                "endpoint": "school.get",
                "status": "success",
                "response_time": round(end_time - start_time, 3),
                "credits_used": 1,
                "sample_fields": {
                    "name": result.get("name", ""),
                    "industry": result.get("industry", ""),
                    "follower_count": result.get("follower_count", 0)
                }
            })
        except Exception as e:
            self.results.append({
                "endpoint": "school.get",
                "status": "error",
                "error": str(e)
            })

    async def test_school_student_list(self):
        """Test school.student_list endpoint"""
        try:
            start_time = time.time()
            result = await self.enrichlayer.school.student_list(
                linkedin_school_url="https://www.linkedin.com/school/national-university-of-singapore"
            )
            end_time = time.time()
            
            self.results.append({
                "endpoint": "school.student_list",
                "status": "success",
                "response_time": round(end_time - start_time, 3),
                "credits_used": 1,
                "sample_fields": {
                    "student_count": len(result.get("students", [])),
                    "has_next_page": bool(result.get("next_page"))
                }
            })
        except Exception as e:
            self.results.append({
                "endpoint": "school.student_list",
                "status": "error",
                "error": str(e)
            })

    # JOB ENDPOINTS
    async def test_job_get(self):
        """Test job.get endpoint"""
        try:
            start_time = time.time()
            # Using a generic job URL - this might need adjustment
            result = await self.enrichlayer.job.get(
                url="https://www.linkedin.com/jobs/view/123456789"
            )
            end_time = time.time()
            
            self.results.append({
                "endpoint": "job.get",
                "status": "success",
                "response_time": round(end_time - start_time, 3),
                "credits_used": 1,
                "sample_fields": {
                    "title": result.get("title", ""),
                    "company": result.get("company", {}).get("name", "") if result.get("company") else ""
                }
            })
        except Exception as e:
            self.results.append({
                "endpoint": "job.get",
                "status": "error",
                "error": str(e)
            })

    # CUSTOMERS ENDPOINTS
    async def test_customers_listing(self):
        """Test customers.listing endpoint"""
        try:
            start_time = time.time()
            result = await self.enrichlayer.customers.listing(
                linkedin_company_profile_url="https://www.linkedin.com/company/apple/"
            )
            end_time = time.time()
            
            self.results.append({
                "endpoint": "customers.listing",
                "status": "success",
                "response_time": round(end_time - start_time, 3),
                "credits_used": 1,
                "sample_fields": {
                    "customer_count": len(result.get("companies", [])) if result.get("companies") else 0
                }
            })
        except Exception as e:
            self.results.append({
                "endpoint": "customers.listing",
                "status": "error",
                "error": str(e)
            })

    async def run_all_tests(self):
        """Run all endpoint tests"""
        print("Starting complete endpoint testing...")
        
        # Credit balance
        await self.test_get_balance()
        
        # Person endpoints (9 methods)
        await self.test_person_get()
        await self.test_person_search()
        await self.test_person_resolve()
        await self.test_person_resolve_by_email()
        await self.test_person_resolve_by_phone()
        await self.test_person_lookup_email()
        await self.test_person_personal_contact()
        await self.test_person_personal_email()
        await self.test_person_profile_picture()
        
        # Company endpoints (9 methods)
        await self.test_company_get()
        await self.test_company_search()
        await self.test_company_resolve()
        await self.test_company_find_job()
        await self.test_company_job_count()
        await self.test_company_employee_count()
        await self.test_company_employee_list()
        await self.test_company_employee_search()
        await self.test_company_role_lookup()
        await self.test_company_profile_picture()
        
        # School endpoints (2 methods)
        await self.test_school_get()
        await self.test_school_student_list()
        
        # Job endpoints (1 method)
        await self.test_job_get()
        
        # Customer endpoints (1 method)
        await self.test_customers_listing()
        
        print(f"Completed {len(self.results)} endpoint tests")
        
    def generate_report(self) -> Dict[str, Any]:
        """Generate comprehensive test report"""
        successful_tests = [r for r in self.results if r["status"] == "success"]
        failed_tests = [r for r in self.results if r["status"] == "error"]
        
        total_credits_used = sum(r.get("credits_used", 0) for r in successful_tests)
        avg_response_time = sum(r.get("response_time", 0) for r in successful_tests) / len(successful_tests) if successful_tests else 0
        
        # Group by endpoint category
        endpoint_categories = {
            "general": [],
            "person": [],
            "company": [],
            "school": [],
            "job": [],
            "customers": []
        }
        
        for result in self.results:
            endpoint = result["endpoint"]
            if endpoint.startswith("person."):
                endpoint_categories["person"].append(result)
            elif endpoint.startswith("company."):
                endpoint_categories["company"].append(result)
            elif endpoint.startswith("school."):
                endpoint_categories["school"].append(result)
            elif endpoint.startswith("job."):
                endpoint_categories["job"].append(result)
            elif endpoint.startswith("customers."):
                endpoint_categories["customers"].append(result)
            else:
                endpoint_categories["general"].append(result)
        
        return {
            "test_summary": {
                "timestamp": datetime.now().isoformat(),
                "total_tests": len(self.results),
                "successful_tests": len(successful_tests),
                "failed_tests": len(failed_tests),
                "success_rate": f"{len(successful_tests)/len(self.results)*100:.1f}%",
                "total_credits_used": total_credits_used,
                "average_response_time": round(avg_response_time, 3)
            },
            "endpoint_categories": {
                category: {
                    "total": len(results),
                    "successful": len([r for r in results if r["status"] == "success"]),
                    "failed": len([r for r in results if r["status"] == "error"])
                }
                for category, results in endpoint_categories.items()
            },
            "successful_endpoints": successful_tests,
            "failed_endpoints": failed_tests,
            "detailed_results": self.results,
            "by_category": endpoint_categories
        }


async def main():
    """Main test execution"""
    api_key = "a3c4354f-6f80-419a-8f8b-67d41d52c746"
    
    tester = CompleteEndpointTester(api_key)
    await tester.run_all_tests()
    
    report = tester.generate_report()
    
    # Save report to file
    with open("complete_endpoint_test_results.json", "w") as f:
        json.dump(report, f, indent=2, default=str)
    
    # Print summary
    print("\n" + "="*60)
    print("COMPLETE ENDPOINT TEST SUMMARY")
    print("="*60)
    print(f"Total Tests: {report['test_summary']['total_tests']}")
    print(f"Successful: {report['test_summary']['successful_tests']}")
    print(f"Failed: {report['test_summary']['failed_tests']}")
    print(f"Success Rate: {report['test_summary']['success_rate']}")
    print(f"Total Credits Used: {report['test_summary']['total_credits_used']}")
    print(f"Average Response Time: {report['test_summary']['average_response_time']}s")
    
    print("\nBY CATEGORY:")
    for category, stats in report['endpoint_categories'].items():
        if stats['total'] > 0:
            print(f"  {category.upper()}: {stats['successful']}/{stats['total']} successful")
    
    if report['failed_endpoints']:
        print(f"\nFAILED ENDPOINTS ({len(report['failed_endpoints'])}):")
        for failed in report['failed_endpoints']:
            print(f"  - {failed['endpoint']}: {failed['error'][:80]}...")
    
    print(f"\nDetailed results saved to: complete_endpoint_test_results.json")


if __name__ == "__main__":
    asyncio.run(main())