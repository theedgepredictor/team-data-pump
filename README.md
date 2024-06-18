# team-data-pump

The `team-data-pump` is a GitHub Action designed to extract team-related endpoints from the `espn-api-orm`. 

- Team Name Fuzzy Matching
- Global Name Definitions
- Unique Teams per League
- Unique Teams per Season
- Team-Venue visual map 
  - Once sport/league/season is selected, generate all of the team venue's on the map
 
**Team Based Feature Store**

For each season get the team schedule. For each game in the schedule get the team statistics. The main thing here is deciding if we want statistics stored at the event level or at the team level. Statistics that are team related for offense or defense should be at team pump level and allows for easy aggregation of team based stats. 

## Resources
- [espn-api-orm](https://pypi.org/project/espn-api-orm/)
- [Github Actions Setup Python](https://github.com/actions/setup-python/tree/main)
- [Github Actions Pricing](https://docs.github.com/en/billing/managing-billing-for-github-actions/about-billing-for-github-actions)
