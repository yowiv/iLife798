# Copilot Instructions for iLife798

## Project Overview

This is a Python automation script for the 慧生活798 (HuiLife798) platform that automatically collects points through:
- Daily check-in
- Watching videos to earn points
- Support for multiple accounts via Qinglong panel

## Environment & Dependencies

### Python Version
- **Required**: Python 3.6+

### Dependencies
```bash
pip install requests
```

The project uses:
- `requests` - For HTTP API calls to the HuiLife798 platform
- Standard Python libraries: `json`, `time`, `os`, `datetime`

## Environment Variables

### HUI798_AUTH (Required)
Authorization token(s) for the HuiLife798 platform.

**Single Account:**
```bash
export HUI798_AUTH='your_authorization_token'
```

**Multiple Accounts:**
Supports multiple delimiters: `&`, `#`, `@`, `|`, `,`
```bash
export HUI798_AUTH='token1&token2&token3'
```

## Running the Script

### Local Execution
```bash
# Set environment variable
export HUI798_AUTH='your_authorization_token'

# Run the script
python iLife798.py
```

### Testing
There are no automated tests in this repository. Manual testing involves:
1. Setting a valid `HUI798_AUTH` token
2. Running `python iLife798.py`
3. Verifying console output for successful check-in and video watching

## Coding Standards & Conventions

### Code Style
- Follow PEP 8 Python style guide
- Use descriptive variable names in both English and Chinese where appropriate
- Include docstrings for all classes and functions
- Use emoji in print statements for better user experience (🚀, ✅, ❌, etc.)

### Error Handling
- Use try-except blocks for API calls
- Provide user-friendly error messages with clear emojis
- Handle login expiration gracefully (code -99)
- Handle rate limiting with automatic retry (code -98)

### API Integration
- Base URL: `https://i.ilife798.com/api/v1/acc/score`
- All requests use JSON payload and specific headers including:
  - `User-Agent: Android_ilife798_2.0.9`
  - `authorization`: The user's auth token
  - `Content-Type: application/json`

### Code Organization
- Single file script: `iLife798.py`
- Main components:
  - `get_auth_from_env()`: Environment variable parsing
  - `HuiLife798` class: Core API interaction
  - `run_single_account()`: Single account task execution
  - `main()`: Entry point and multi-account orchestration

### Timing & Rate Limiting
- 5-second wait between video watches
- 10-second wait between check-in and video watching
- 15-second wait between different accounts
- Automatic 5-second retry on rate limit error (code -98)

## Key Features to Maintain

1. **Multi-Account Support**: Parse multiple auth tokens from environment variable with various delimiters
2. **Graceful Error Handling**: Handle login expiration and rate limiting
3. **User-Friendly Output**: Use emojis and clear formatting in console output
4. **Qinglong Panel Compatibility**: Script should work in Qinglong cron environment

## File Structure

```
iLife798/
├── .github/
│   └── copilot-instructions.md    # This file
├── iLife798.py                     # Main automation script
└── README.md                       # Project documentation (in Chinese)
```

## Important Notes

- Do not commit authorization tokens or sensitive data
- Maintain backward compatibility with Python 3.6+
- Keep the single-file structure for easy deployment to Qinglong panel
- All user-facing messages should be in Chinese
- Preserve the emoji-based logging style for consistency
