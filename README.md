# Trackable Short URL

The primary purpose of this project is to convert a long URL into a shorter one and also provide session-based cookies to track URL visits.


The program takes a URL and produces a mapping relation to a shorter one; it uses a global sequence number from Redis to ensure there is no duplicated short URL in the cluster; it also stores the relationship from the short URL to the long URL in Redis DB.

## Feature
1. The project features a non-relational database, Redis, which results in higher performance, availability, scalability, and flexibility.
2. The program also keeps track of the statistical information of users; it records dates, times, session IDs, devices, browsers, IP addresses, and URLs. This information can provide detailed statistics regarding service usage and track the relationship of customer behavior, e.g., users visit some jobs on "LinkedIn" and "indeed."
## Main Contributors
* Haoyuan Liu, hl163@rice.edu

## Installation
### Pre-condition
1. One machine with python 3.0+ installed
2. Redis database was installed and is accessible from the machine

### Installation Steps
1. Copy all directories & files to a target machine
2. Install dependent python libs
> pip install -r requirements.txt
3. Config key parameters in HttpShortURL.py

| Parameters          | Description              | Default   |
|:--------------------|:-------------------------|:----------|
| hostName            | hostname of this service | localhost |
| serverPort          | port of this service     | 8080      |
| redisHost           | hostname of redis DB     | localhost |
| redisPort           | port of redis DB         | 8080      |
| redisAuthentication | password of redis DB     | None      |

4. Start the service
> python HttpShortURL.py

## Usage
* Visit http://localhost:8080/
* To create a new short URL: input original URL (Must have) & Label (optional), and click submit
* To access the shorten URL, Visit the links for example, http://localhost:8080/r/SAMPLE
* Visit short URL logs ./logs/ with name ShortUrlVisit-YYYYMMDD.csv, the default CSV fields are:
  * Date Time & TZ
  * clientAddress
  * label
  * session
  * user_agent.browser.family
  *  user_agent.browser.version_string
  *  user_agent.os.family
  *  user_agent.os.version_string
  *  user_agent.device.family
  *  user_agent.device.brand
  *  user_agent.device.model
  *  shortURLCode
  *  longURL

## License
MIT