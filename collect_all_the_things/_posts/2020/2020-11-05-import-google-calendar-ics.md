---
layout: default
title: "Extract ICS from Google Calendars"
categories:
- Google
- Nextcloud
---

I wanted to import the [Openshift.tv Google Calendar][otvgcalendar] to my Nextcloud calendar app. The URL looks like this:

```
https://calendar.google.com/calendar/embed?src=redhatstreaming@gmail.com
```

A simple import in Nextclouds calendar app didn't work, I figured I needed to get either an ICS or ICAL file, but couldn't find any easy way. No button on the website, no knowledge base entries either.  
By chance, I found [a thread][gsuppforum] in Googles support forum which describes a way how to extract the ICS from a Google calendar:

> 1. Go to the settings for the Other Calendar, and note down the Public URL to this calendar, for example: `https://calendar.google.com/calendar/embed?src=en-gb.christian%23holiday%40group.v.calendar.google.com&ctz=Europe%2FParis`
>
> 2. Now take the part after 'src=' up to and including `calendar.google.com` so in this case our subscribed calendar ID is `en-gb.christian%23holiday%40group.v.calendar.google.com`
>
> 3. Now replace the \*\*\*\*\*\*\*\*\*\* here with that text: `https://calendar.google.com/calendar/ical/**********/public/basic.ics` to give the final feed URL which you can download directly in your browser: `https://calendar.google.com/calendar/ical/en-gb.christian%23holiday%40group.v.calendar.google.com/public/basic.ics`

For the Openshift.tv calendar, this lead to this ICAL URL: `https://calendar.google.com/calendar/ical/redhatstreaming@gmail.com/public/basic.ics`

[otvgcalendar]: https://calendar.google.com/calendar/embed?src=redhatstreaming@gmail.com
[gsuppforum]: https://support.google.com/calendar/thread/7353749?msgid=17912822
