# DPVerFetch
DigiPen Version Control Update Discord Webhook

## About:
This script loops every 30 seconds and sends a separate discord message for each version control update in the given repository.

## How to Use:
- Get a Discord webhook URL.
```
 - [Right Click] channel
 - [Edit Channel]
 - [Integrations]
 - Webhooks -> [Create Webhook]
 - [Captain Hook]
 - Give it a cute name.
 - [Copy Webhook URL]
```
- Populate .env with the labeled fields. Unless you have specific credentials for bot access, your personal credentials may be necessary.
> This script is configured for SVN tracking. To convert to git tracking, change the domain in .env to trac-git.digipen.edu.
- Run VerFetch.py.

**Please credit me for my work. Don't tell your friends you made this.**
