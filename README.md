# `enrichlayer-api` -  The official Python client for Enrich Layer API to scrape and enrich LinkedIn profiles

* [What is Enrich Layer?](#what-is-enrich-layer-)
* [Before you install](#before-you-install)
* [Installation and supported Python versions](#installation-and-supported-python-versions)
* [Initializing `enrichlayer-api` with an API Key](#initializing--enrichlayer-api--with-an-api-key)
* [Usage with examples](#usage-with-examples)
  + [Enrich a Person Profile](#enrich-a-person-profile)
  + [Enrich a Company Profile](#enrich-a-company-profile)
  + [Lookup a person](#lookup-a-person)
  + [Lookup a company](#lookup-a-company)
  + [Lookup a LinkedIn Profile URL from a work email address](#lookup-a-linkedin-profile-url-from-a-work-email-address)
  + [Enrich LinkedIn member profiles in bulk (from a CSV)](#enrich-linkedin-member-profiles-in-bulk--from-a-csv-)
  + [More *asyncio* examples](#more--asyncio--examples)
* [Rate limit and error handling](#rate-limit-and-error-handling)
* [API Endpoints and their corresponding documentation](#api-endpoints-and-their-corresponding-documentation)

## What is Enrich Layer?

**Enrich Layer** is an enrichment API to fetch fresh data on people and businesses. We are a fully-managed API that sits between your application and raw data so that you can focus on building the application; instead of worrying about building a web-scraping team and processing data at scale.

With Enrich Layer, you can programatically:

- Enrich profiles on people and companies
- Lookup people and companies
- Lookup contact information on people and companies
- Check if an email address is of a disposable nature
- [And more..](https://enrichlayer.com/docs/pc#explain-it-to-me-like-i-39-m-5)

Visit [Enrich Layer&#39;s website](https://enrichlayer.com) for more details.

## Before you install

You should understand that `enrichlayer-api` was designed with concurrency as a first class citizen from ground-up. To install `enrichlayer-api`, *you have to pick a concurency model*.

We support the following concurrency models:

* [asyncio](https://docs.python.org/3/library/asyncio.html) - See implementation example [here](examples/lib-asyncio.py).
* [gevent](https://www.gevent.org/) - See implementation example [here](examples/lib-gevent.py).
* [twisted](https://twisted.org/) - See implementation example [here](examples/lib-twisted.py).

The right way to use Enrich Layer API is to make API calls concurrently. In fact, making API requests concurrently is the only way to achieve a high rate of throughput. On the default rate limit, you can enrich up to 432,000 profiles per day. See [this blog post](https://enrichlayer.com/blog/how-to-maximize-throughput-on-enrichlayer/) for context.

## Installation and supported Python versions

`enrichlayer-api` is [available on PyPi](https://pypi.org/project/enrichlayer-api/). For which you can install into your project with the following command:

```bash
# install enrichlayer-api with asyncio
$ pip install 'enrichlayer-api[asyncio]'

# install enrichlayer-api with gevent
$ pip install 'enrichlayer-api[gevent]'

# install enrichlayer-api with twisted
$ pip install 'enrichlayer-api[twisted]'
```

`enrichlayer-api` is tested on Python `3.7`, `3.8` and `3.9`.

## Initializing `enrichlayer-api` with an API Key

You can get an API key by [registering an account](https://enrichlayer.com/auth/register) with Enrich Layer. The API Key can be retrieved from the dashboard.

To use Enrich Layer with the API Key:

* You can run your script with  the `ENRICHLAYER_API_KEY` environment variable set.
* Or, you can prepend your script with the API key injected into the environment. See `enrichlayer/config.py` for an example.

## Usage with examples

I will be using `enrichlayer-api` with the *asyncio* concurrency model to illustrate some examples on what you can do with Enrich Layer and how the code will look with this library.

Forexamples with other concurrency models such as:

* *gevent*, see `examples/lib-gevent.py`.
* *twisted*, see `examples/lib-twisted`.

### Enrich a Person Profile

Given a *LinkedIn Member Profile URL*, you can get the entire profile back in structured data with Enrich Layer's [Person Profile API Endpoint](https://enrichlayer.com/docs/pc#people-api-person-profile-endpoint).

```python
from enrichlayer.asyncio import EnrichLayer, do_bulk
import asyncio
import csv

enrichlayer = EnrichLayer()
person = asyncio.run(enrichlayer.person.get(
    linkedin_profile_url='https://www.linkedin.com/in/williamhgates/'
))
print('Person Result:', person)
```

### Enrich a Company Profile

Given a *LinkedIn Company Profile URL*, enrich the URL with it's full profile with Enrich Layer's [Company Profile API Endpoint](https://enrichlayer.com/docs/pc#company-api-company-profile-endpoint).

```python
company = asyncio.run(enrichlayer.company.get(
    url='https://www.linkedin.com/company/tesla-motors'
))
print('Company Result:', company)
```

### Lookup a person

Given a first name and a company name or domain, lookup a person with Enrich Layer's [Person Lookup API Endpoint](https://enrichlayer.com/docs/pc#people-api-person-lookup-endpoint).

```python
lookup_results = asyncio.run(enrichlayer.person.resolve(first_name="bill", last_name="gates", company_domain="microsoft"))
print('Person Lookup Result:', lookup_results)
```

### Lookup a company

Given a company name or a domain, lookup a company with Enrich Layer's [Company Lookup API Endpoint](https://enrichlayer.com/docs/pc#company-api-company-lookup-endpoint).

```python
company_lookup_results = asyncio.run(enrichlayer.company.resolve(company_name="microsoft", company_domain="microsoft.com"))
print('Company Lookup Result:', company_lookup_results)
```

### Lookup a LinkedIn Profile URL from a work email address

Given a work email address, lookup a LinkedIn Profile URL with Enrich Layer's [Reverse Work Email Lookup Endpoint](https://enrichlayer.com/docs/pc#contact-api-reverse-work-email-lookup-endpoint).

```python
lookup_results = asyncio.run(enrichlayer.person.resolve_by_email(work_email="anthony.tan@grab.com"))
print('Reverse Work Email Lookup Result:', lookup_results)
```

### Enrich LinkedIn member profiles in bulk (from a CSV)

Given a CSV file with a list of LinkedIn member profile URLs, you can enrich the list in the following manner:

```python
# PROCESS BULK WITH CSV
bulk_linkedin_person_data = []
with open('sample.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader, None)
    for row in reader:
        bulk_linkedin_person_data.append(
            (enrichlayer.person.get, {'url': row[0]})
        )
results = asyncio.run(do_bulk(bulk_linkedin_person_data))

print('Bulk:', results)
```

### More *asyncio* examples

More *asyncio* examples can be found at `examples/lib-asyncio.py`

## Rate limit and error handling

There is no need for you to handle rate limits (`429` HTTP status error). The library handles rate limits automatically with exponential backoff.

However, there is a need for you to handle other error codes. Errors will be returned in the form of `EnrichLayerException`. The [list of possible errors](https://enrichlayer.com/docs/pc#overview-errors) is listed in our API documentation.

## API Endpoints and their corresponding documentation

Here we list the possible API endpoints and their corresponding library functions. Do refer to each endpoint's relevant API documentation to find out the required arguments that needs to be fed into the function.

| Function                                       | Endpoint                                                                                                                     | API                                                      |
| ---------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------- |
| `company.employee_count(**kwargs)`  | [Employee Count Endpoint](https://enrichlayer.com/docs/pc#company-api-employee-count-endpoint)                                 | [Company API](https://enrichlayer.com/docs/pc#company-api) |
| `company.resolve(**kwargs)`         | [Company Lookup Endpoint](https://enrichlayer.com/docs/pc#company-api-company-profile-endpoint)                                | [Company API](https://enrichlayer.com/docs/pc#company-api) |
| `company.employee_list(**kwargs)`   | [Employee Listing Endpoint](https://enrichlayer.com/docs/pc#company-api-employee-listing-endpoint)                             | [Company API](https://enrichlayer.com/docs/pc#company-api) |
| `company.get(**kwargs)`             | [Company Profile Endpoint](https://enrichlayer.com/docs/pc#company-api-company-profile-endpoint)                               | [Company API](https://enrichlayer.com/docs/pc#company-api) |
| `person.resolve_by_email(**kwargs)` | [Reverse Work Email Lookup Endpoint](https://enrichlayer.com/docs/pc#contact-api-reverse-work-email-lookup-endpoint)           | [Contact API](https://enrichlayer.com/docs/pc#contact-api) |
| `person.lookup_email(**kwargs)`     | [Work Email Lookup Endpoint](https://enrichlayer.com/docs/pc#contact-api-work-email-lookup-endpoint)                           | [Contact API](https://enrichlayer.com/docs/pc#contact-api) |
| `person.personal_contact(**kwargs)` | [Personal Contact Number Lookup Endpoint](https://enrichlayer.com/docs/pc#contact-api-personal-contact-number-lookup-endpoint) | [Contact API](https://enrichlayer.com/docs/pc#contact-api) |
| `person.personal_email(**kwargs)`   | [Personal Email Lookup Endpoint](https://enrichlayer.com/docs/pc#contact-api-personal-email-lookup-endpoint)                   | [Contact API](https://enrichlayer.com/docs/pc#contact-api) |
| `disposable_email(**kwargs)`        | [Disposable Email Address Check Endpoint](https://enrichlayer.com/docs/pc#contact-api-disposable-email-address-check-endpoint) | [Contact API](https://enrichlayer.com/docs/pc#contact-api) |
| `company.find_job(**kwargs)`        | [Job Listings Endpoint](https://enrichlayer.com/docs/pc#jobs-api-jobs-listing-endpoint)                                        | [Jobs API](https://enrichlayer.com/docs/pc#jobs-api)       |
| `job.get(**kwargs)`                 | [Jobs Profile Endpoint](https://enrichlayer.com/docs/pc#jobs-api-job-profile-endpoint)                                         | [Jobs API](https://enrichlayer.com/docs/pc#jobs-api)       |
| `person.resolve(**kwargs)`          | [Person Lookup Endpoint](https://enrichlayer.com/docs/pc#people-api-person-lookup-endpoint)                                    | [People API](https://enrichlayer.com/docs/pc#people-api)   |
| `company.role_lookup(**kwargs)`     | [Role Lookup Endpoint](https://enrichlayer.com/docs/pc#people-api-role-lookup-endpoint)                                        | [People API](https://enrichlayer.com/docs/pc#people-api)   |
| `person.get(**kwargs)`              | [Person Profile Endpoint](https://enrichlayer.com/docs/pc#people-api-person-profile-endpoint)                                  | [People API](https://enrichlayer.com/docs/pc#people-api)   |
| `school.get(**kwargs)`              | [School Profile Endpoint](https://enrichlayer.com/docs/pc#school-api-school-profile-endpoint)                                  | [School API](https://enrichlayer.com/docs/pc#school-api)   |
| `company.reveal`                    | [Reveal Endpoint](https://enrichlayer.com/docs/pc#reveal-api-reveal-endpoint)                                                  | [Reveal API](https://enrichlayer.com/docs/pc#reveal-api)   |
| `get_balance(**kwargs)`                      | [View Credit Balance Endpoint](https://enrichlayer.com/docs/pc#meta-api-view-credit-balance-endpoint)                          | [Meta API](https://enrichlayer.com/docs/pc#meta-api)       |

## Proxycurl-py Compatibility

For users migrating from `proxycurl-py`, `enrichlayer-api` provides a compatibility layer that allows existing code to work unchanged while using the new EnrichLayer backend.

### Setup

Install both packages:

```bash
pip install enrichlayer-api
pip install proxycurl-py
```

### Usage

Enable compatibility mode in your existing code by adding one import line:

```python
import enrichlayer
enrichlayer.enable_proxycurl_compatibility()

# Now your existing proxycurl-py code works unchanged
from proxycurl.asyncio import Proxycurl, do_bulk
proxycurl = Proxycurl()

# All existing methods work exactly the same
person = asyncio.run(proxycurl.linkedin.person.get(
    linkedin_profile_url='https://www.linkedin.com/in/williamhgates/'
))
company = asyncio.run(proxycurl.linkedin.company.get(
    url='https://www.linkedin.com/company/apple'
))
```

### Configuration Options

```python
# Enable with custom configuration
enrichlayer.enable_proxycurl_compatibility(
    api_key='your-api-key',
    base_url='https://enrichlayer.com/api/v2',
    deprecation_warnings=True  # Show migration warnings
)
```

### Migration Path

1. **Immediate**: Add `enrichlayer.enable_proxycurl_compatibility()` to existing code
2. **Gradual**: Replace imports one by one:
   ```python
   # Old: from proxycurl.asyncio import Proxycurl
   # New: from enrichlayer.asyncio import EnrichLayer as Proxycurl
   ```
3. **Complete**: Use the new direct API structure:
   ```python
   # Old: proxycurl.linkedin.person.get(...)
   # New: enrichlayer.person.get(...)
   ```

### Environment Variables

The compatibility layer supports both old and new environment variables:
- `PROXYCURL_API_KEY` (legacy)
- `ENRICHLAYER_API_KEY` (new)

### Benefits

- **Zero Breaking Changes**: Existing code works immediately
- **Modern Backend**: Benefits from improved EnrichLayer infrastructure  
- **Flexible Migration**: Migrate at your own pace
- **Future-Proof**: Easy path to new API structure
