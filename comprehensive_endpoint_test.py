#!/usr/bin/env python3
"""
Comprehensive endpoint testing for enrichlayer_client.

This script tests all available endpoints systematically and generates
a detailed report of their functionality and response structure.
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


class EndpointTester:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.enrichlayer = EnrichLayer(api_key=api_key)
        self.results = []
        
    async def test_credit_balance(self):
        """Test credit balance endpoint"""
        try:
            start_time = time.time()
            result = await self.enrichlayer.get_balance()
            end_time = time.time()
            
            self.results.append({
                "endpoint": "credit_balance",
                "status": "success",
                "response_time": round(end_time - start_time, 3),
                "credits_used": 0,
                "response_structure": {
                    "credit_balance": type(result.get("credit_balance", 0)).__name__
                },
                "sample_data": result
            })
        except Exception as e:
            self.results.append({
                "endpoint": "credit_balance",
                "status": "error",
                "error": str(e),
                "response_time": None
            })

    async def test_person_profile(self):
        """Test person profile endpoint"""
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
                "response_structure": {
                    "full_name": type(result.get("full_name", "")).__name__,
                    "headline": type(result.get("headline", "")).__name__,
                    "experiences": type(result.get("experiences", [])).__name__,
                    "education": type(result.get("education", [])).__name__,
                    "skills": type(result.get("skills", [])).__name__
                },
                "sample_fields": {
                    "full_name": result.get("full_name", ""),
                    "headline": result.get("headline", "")[:100] if result.get("headline") else None,
                    "experience_count": len(result.get("experiences", [])),
                    "education_count": len(result.get("education", [])),
                    "skills_count": len(result.get("skills", []))
                }
            })
        except Exception as e:
            self.results.append({
                "endpoint": "person.get",
                "status": "error",
                "error": str(e),
                "test_url": test_url,
                "response_time": None
            })

    async def test_company_profile(self):
        """Test company profile endpoint"""
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
                "test_url": test_url,
                "response_structure": {
                    "name": type(result.get("name", "")).__name__,
                    "description": type(result.get("description", "")).__name__,
                    "industry": type(result.get("industry", "")).__name__,
                    "company_size": type(result.get("company_size", [])).__name__,
                    "locations": type(result.get("locations", [])).__name__
                },
                "sample_fields": {
                    "name": result.get("name", ""),
                    "industry": result.get("industry", ""),
                    "company_size": result.get("company_size", []),
                    "founded_year": result.get("founded_year", None),
                    "follower_count": result.get("follower_count", None)
                }
            })
        except Exception as e:
            self.results.append({
                "endpoint": "company.get",
                "status": "error",
                "error": str(e),
                "test_url": test_url,
                "response_time": None
            })

    async def test_company_with_extras(self):
        """Test company profile with extra data"""
        test_url = "https://www.linkedin.com/company/apple/"
        try:
            start_time = time.time()
            result = await self.enrichlayer.company.get(
                url=test_url,
                extra="include",
                funding_data="include",
                categories="include"
            )
            end_time = time.time()
            
            self.results.append({
                "endpoint": "company.get_with_extras",
                "status": "success",
                "response_time": round(end_time - start_time, 3),
                "credits_used": 4,  # 1 base + 1 extra + 1 funding + 1 categories
                "test_url": test_url,
                "parameters": {
                    "extra": "include",
                    "funding_data": "include", 
                    "categories": "include"
                },
                "response_structure": {
                    "extra": type(result.get("extra", {})).__name__,
                    "funding_data": type(result.get("funding_data", {})).__name__,
                    "categories": type(result.get("categories", [])).__name__
                },
                "sample_fields": {
                    "has_extra_data": bool(result.get("extra")),
                    "has_funding_data": bool(result.get("funding_data")),
                    "categories_count": len(result.get("categories", []))
                }
            })
        except Exception as e:
            self.results.append({
                "endpoint": "company.get_with_extras",
                "status": "error",
                "error": str(e),
                "test_url": test_url,
                "response_time": None
            })

    async def test_employee_listing(self):
        """Test employee listing endpoint"""
        test_url = "https://www.linkedin.com/company/apple/"
        try:
            start_time = time.time()
            result = await self.enrichlayer.company.employee_list(url=test_url)
            end_time = time.time()
            
            employees = result.get("employees", [])
            
            self.results.append({
                "endpoint": "company.employee_list",
                "status": "success",
                "response_time": round(end_time - start_time, 3),
                "credits_used": 1,
                "test_url": test_url,
                "response_structure": {
                    "employees": type(employees).__name__,
                    "next_page": type(result.get("next_page", "")).__name__
                },
                "sample_fields": {
                    "employee_count": len(employees),
                    "has_next_page": bool(result.get("next_page")),
                    "first_employee": employees[0] if employees else None
                }
            })
        except Exception as e:
            self.results.append({
                "endpoint": "company.employee_list",
                "status": "error",
                "error": str(e),
                "test_url": test_url,
                "response_time": None
            })

    async def test_employee_count(self):
        """Test employee count endpoint"""
        test_url = "https://www.linkedin.com/company/apple/"
        try:
            start_time = time.time()
            result = await self.enrichlayer.company.employee_count(url=test_url)
            end_time = time.time()
            
            self.results.append({
                "endpoint": "company.employee_count",
                "status": "success", 
                "response_time": round(end_time - start_time, 3),
                "credits_used": 1,
                "test_url": test_url,
                "response_structure": {
                    "total_employee": type(result.get("total_employee", 0)).__name__,
                    "linkedin_employee_count": type(result.get("linkedin_employee_count", 0)).__name__,
                    "linkdb_employee_count": type(result.get("linkdb_employee_count", 0)).__name__
                },
                "sample_data": result
            })
        except Exception as e:
            self.results.append({
                "endpoint": "company.employee_count",
                "status": "error",
                "error": str(e),
                "test_url": test_url,
                "response_time": None
            })

    async def test_person_lookup_url_enrich(self):
        """Test person lookup URL enrich endpoint"""
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
                "parameters": {
                    "first_name": "Bill",
                    "last_name": "Gates", 
                    "company_domain": "microsoft.com"
                },
                "response_structure": {
                    "url": type(result.get("url", "")).__name__,
                    "name_similarity_score": type(result.get("name_similarity_score", 0.0)).__name__,
                    "profile": type(result.get("profile", {})).__name__
                },
                "sample_fields": {
                    "found_url": result.get("url", ""),
                    "name_similarity": result.get("name_similarity_score", 0.0),
                    "has_profile": bool(result.get("profile"))
                }
            })
        except Exception as e:
            self.results.append({
                "endpoint": "person.resolve",
                "status": "error",
                "error": str(e),
                "response_time": None
            })

    async def test_person_email_lookup(self):
        """Test person email lookup endpoint"""
        try:
            start_time = time.time()
            result = await self.enrichlayer.person.lookup_email(
                email="bill@microsoft.com"
            )
            end_time = time.time()
            
            self.results.append({
                "endpoint": "person.lookup_email",
                "status": "success",  
                "response_time": round(end_time - start_time, 3),
                "credits_used": 1,
                "test_email": "bill@microsoft.com",
                "response_structure": {
                    "linkedin_profile_url": type(result.get("linkedin_profile_url", "")).__name__,
                    "profile": type(result.get("profile", {})).__name__
                },
                "sample_data": {k: v for k, v in result.items() if k not in ["profile"]}
            })
        except Exception as e:
            self.results.append({
                "endpoint": "person.lookup_email",
                "status": "error",
                "error": str(e),
                "response_time": None
            })

    async def test_school_profile(self):
        """Test school profile endpoint"""
        test_url = "https://www.linkedin.com/school/national-university-of-singapore"
        try:
            start_time = time.time()
            result = await self.enrichlayer.school.get(url=test_url)
            end_time = time.time()
            
            self.results.append({
                "endpoint": "school.get",
                "status": "success",
                "response_time": round(end_time - start_time, 3),
                "credits_used": 1,
                "test_url": test_url,
                "response_structure": {
                    "name": type(result.get("name", "")).__name__,
                    "description": type(result.get("description", "")).__name__,
                    "website": type(result.get("website", "")).__name__,
                    "industry": type(result.get("industry", "")).__name__
                },
                "sample_fields": {
                    "name": result.get("name", ""),
                    "industry": result.get("industry", ""),
                    "founded_year": result.get("founded_year", None),
                    "follower_count": result.get("follower_count", None)
                }
            })
        except Exception as e:
            self.results.append({
                "endpoint": "school.get",
                "status": "error",
                "error": str(e),
                "test_url": test_url,
                "response_time": None
            })

    async def run_all_tests(self):
        """Run all endpoint tests"""
        print("Starting comprehensive endpoint testing...")
        
        # Test basic endpoints
        await self.test_credit_balance()
        await self.test_person_profile()
        await self.test_company_profile()
        await self.test_company_with_extras()
        await self.test_employee_listing()
        await self.test_employee_count()
        await self.test_person_lookup_url_enrich()
        await self.test_person_email_lookup()
        await self.test_school_profile()
        
        print(f"Completed {len(self.results)} endpoint tests")
        
    def generate_report(self) -> Dict[str, Any]:
        """Generate comprehensive test report"""
        successful_tests = [r for r in self.results if r["status"] == "success"]
        failed_tests = [r for r in self.results if r["status"] == "error"]
        
        total_credits_used = sum(r.get("credits_used", 0) for r in successful_tests)
        avg_response_time = sum(r.get("response_time", 0) for r in successful_tests) / len(successful_tests) if successful_tests else 0
        
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
            "successful_endpoints": successful_tests,
            "failed_endpoints": failed_tests,
            "detailed_results": self.results
        }


async def main():
    """Main test execution"""
    api_key = "a3c4354f-6f80-419a-8f8b-67d41d52c746"
    
    tester = EndpointTester(api_key)
    await tester.run_all_tests()
    
    report = tester.generate_report()
    
    # Save report to file
    with open("endpoint_test_results.json", "w") as f:
        json.dump(report, f, indent=2, default=str)
    
    # Print summary
    print("\n" + "="*60)
    print("ENDPOINT TEST SUMMARY")
    print("="*60)
    print(f"Total Tests: {report['test_summary']['total_tests']}")
    print(f"Successful: {report['test_summary']['successful_tests']}")
    print(f"Failed: {report['test_summary']['failed_tests']}")
    print(f"Success Rate: {report['test_summary']['success_rate']}")
    print(f"Total Credits Used: {report['test_summary']['total_credits_used']}")
    print(f"Average Response Time: {report['test_summary']['average_response_time']}s")
    
    if report['failed_endpoints']:
        print("\nFAILED ENDPOINTS:")
        for failed in report['failed_endpoints']:
            print(f"  - {failed['endpoint']}: {failed['error']}")
    
    print(f"\nDetailed results saved to: endpoint_test_results.json")


if __name__ == "__main__":
    asyncio.run(main())