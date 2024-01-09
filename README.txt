Goal:
Code a bot to generate somewhat sensible biographies for US Physics Team members.
https://www.aapt.org/physicsteam/2023/physics_team_2023.cfm

Process:
- Read the student biographies of candidates from 2023
- Parse biographies into sentences
- Convert words into bigram frequencies
- Create discrete system of some sort based on these frequencies
- Implement some sort of iterator to generate text on demand
