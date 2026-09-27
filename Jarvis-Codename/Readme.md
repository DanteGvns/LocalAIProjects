# Event Parser

A local AI-powered tool to parse natural language event descriptions into structured event objects.

## Description

This project creates a parser that takes natural language strings containing event details (e.g., due dates, times) and converts them into standardized output format using local AI models. Designed for privacy-conscious environments where offline processing is required.

## How It Works

The parser uses a local language model to:
1. Identify key event components (subject, type, due date, time)
2. Calculate date offsets (e.g., "tomorrow" → next calendar day)
3. Format output into a consistent string

## Example

**Input:**  
`(Current Date/Time = 9/27/2026, 4:11pm) I have a Computer Networking assignment due tomorrow at 9pm`

**Output:**  
`(Computer Networking, Homework, 9/28/2026, 9pm)`
