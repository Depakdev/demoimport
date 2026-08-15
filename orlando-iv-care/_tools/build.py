#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Orlando IV Care — static site generator (OPTIONAL TOOL)
--------------------------------------------------------------------------
The website in this folder is plain HTML/CSS/JS and can be edited directly.
This script only exists so the shared header/footer/CTA blocks stay in sync
if you ever want to regenerate every page at once.

  python3 _tools/build.py

WARNING: running this OVERWRITES the generated .html files.
Edit the HTML directly if you are not using this script.
"""

import html
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ==========================================================================
#  SITE CONFIG  —  >>> EDIT ME <<<  (business details used across the site)
# ==========================================================================
SITE = {
    "name": "Orlando IV Care",
    "tagline": "Premium Mobile IV Therapy in Orlando",
    "domain": "https://www.orlandoivcare.com",
    "phone_display": "(407) 000-0000",
    "phone_href": "+14070000000",
    "email": "hello@orlandoivcare.com",
    "hours": "Every day, 8:00am – 9:00pm",
    "facebook": "https://www.facebook.com/",
    "instagram": "https://www.instagram.com/",
}

EDIT_ME = ("<!-- >>> EDIT ME: phone number, email and booking links are set in one place. "
           "Search this file for \"" + SITE["phone_display"] + "\" and \"" + SITE["email"] + "\". <<< -->")


# ==========================================================================
#  ICONS  (Lucide-style, single family, 1.75 stroke)
# ==========================================================================
def icon(name, size=24, cls=""):
    paths = ICONS.get(name, "")
    c = ' class="%s"' % cls if cls else ""
    return ('<svg%s xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 24 24" '
            'fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" '
            'stroke-linejoin="round" aria-hidden="true" focusable="false">%s</svg>') % (c, size, size, paths)


ICONS = {
    "arrow-right": '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>',
    "arrow-left": '<path d="M19 12H5"/><path d="m12 19-7-7 7-7"/>',
    "x": '<path d="M18 6 6 18"/><path d="m6 6 12 12"/>',
    "chevron-down": '<path d="m6 9 6 6 6-6"/>',
    "chevron-left": '<path d="m15 18-6-6 6-6"/>',
    "chevron-right": '<path d="m9 18 6-6-6-6"/>',
    "plus": '<path d="M5 12h14"/><path d="M12 5v14"/>',
    "check": '<path d="M20 6 9 17l-5-5"/>',
    "check-circle": '<circle cx="12" cy="12" r="9"/><path d="m8.5 12.5 2.5 2.5 4.5-5"/>',
    "shield-check": '<path d="M12 3 5 6v5.5c0 4.2 2.9 8.1 7 9.5 4.1-1.4 7-5.3 7-9.5V6z"/><path d="m9 12 2 2 4-4"/>',
    "stethoscope": '<path d="M4.8 3H3v5a4.2 4.2 0 0 0 8.4 0V3H9.6"/><path d="M7.2 12.2v2.3a5.5 5.5 0 0 0 11 0v-1.1"/><circle cx="18.2" cy="10.6" r="2.2"/>',
    "car": '<path d="M5 13 6.6 8.4A2 2 0 0 1 8.5 7h7a2 2 0 0 1 1.9 1.4L19 13"/><path d="M4 13h16v4a1 1 0 0 1-1 1h-1.5a1 1 0 0 1-1-1v-1h-9v1a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1z"/><path d="M7 16h.01"/><path d="M17 16h.01"/>',
    "zap": '<path d="M13 2 4.5 13H11l-.9 9L19 11h-6.4z"/>',
    "droplet": '<path d="M12 2.7 6.9 8.3a7 7 0 1 0 10.2 0z"/>',
    "heart": '<path d="M19.3 5.7a4.6 4.6 0 0 0-6.5 0l-.8.8-.8-.8a4.6 4.6 0 0 0-6.5 6.5l7.3 7.4 7.3-7.4a4.6 4.6 0 0 0 0-6.5z"/>',
    "calendar": '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M8 3v4"/><path d="M16 3v4"/><path d="M3 10h18"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.2 1.9"/>',
    "phone": '<path d="M15.6 21A13.6 13.6 0 0 1 3 8.4 2.4 2.4 0 0 1 5.4 6h1.9a1.6 1.6 0 0 1 1.6 1.4c.1.9.3 1.7.6 2.5a1.6 1.6 0 0 1-.4 1.7l-.9.9a12 12 0 0 0 4.3 4.3l.9-.9a1.6 1.6 0 0 1 1.7-.4c.8.3 1.6.5 2.5.6A1.6 1.6 0 0 1 19 17.7v1.9A2.4 2.4 0 0 1 15.6 21z"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3.5 6.5 8.5 6 8.5-6"/>',
    "map-pin": '<path d="M12 21s7-5.6 7-11a7 7 0 1 0-14 0c0 5.4 7 11 7 11z"/><circle cx="12" cy="10" r="2.6"/>',
    "star": '<path d="m12 3.5 2.6 5.4 5.9.8-4.3 4.1 1 5.9-5.2-2.8-5.2 2.8 1-5.9L3.5 9.7l5.9-.8z" fill="currentColor" stroke="none"/>',
    "user-check": '<path d="M15.5 20v-1.6a3.4 3.4 0 0 0-3.4-3.4H6.9a3.4 3.4 0 0 0-3.4 3.4V20"/><circle cx="9.5" cy="8" r="3.4"/><path d="m16.5 11.5 1.8 1.8 3.2-3.6"/>',
    "brain": '<path d="M9.5 3.5A2.5 2.5 0 0 0 7 6v.2A2.7 2.7 0 0 0 4.6 9c0 .8.3 1.5.8 2A2.8 2.8 0 0 0 6 16.4a2.6 2.6 0 0 0 2.6 2.6c.6 0 1.2-.2 1.7-.6V3.7a2.4 2.4 0 0 0-.8-.2z"/><path d="M14.5 3.5A2.5 2.5 0 0 1 17 6v.2A2.7 2.7 0 0 1 19.4 9c0 .8-.3 1.5-.8 2a2.8 2.8 0 0 1 .4 5.4 2.6 2.6 0 0 1-2.6 2.6c-.6 0-1.2-.2-1.7-.6V3.7c.2-.1.5-.2.8-.2z"/>',
    "shield": '<path d="M12 3 5 6v5.5c0 4.2 2.9 8.1 7 9.5 4.1-1.4 7-5.3 7-9.5V6z"/>',
    "battery-low": '<rect x="2.5" y="7.5" width="16" height="9" rx="2"/><path d="M21.5 11v2"/><path d="M5.5 10.5v3"/>',
    "flame": '<path d="M12 21a5.6 5.6 0 0 0 5.6-5.6c0-4.4-4-5.6-3.2-9.4-2.5.6-4 2.6-4 4.6 0 1.3.5 2 .5 2.7a1.6 1.6 0 0 1-2.8 1c-.6 1-1.7 1.4-1.7 3.4A5.4 5.4 0 0 0 12 21z"/>',
    "dna": '<path d="M6 3c0 4 12 5 12 9s-12 5-12 9"/><path d="M18 3c0 4-12 5-12 9s12 5 12 9"/><path d="M8.5 6.5h7"/><path d="M8.5 17.5h7"/>',
    "citrus": '<circle cx="12" cy="12" r="9"/><path d="M12 3v18"/><path d="M3 12h18"/><path d="m5.6 5.6 12.8 12.8"/><path d="M18.4 5.6 5.6 18.4"/>',
    "sparkles": '<path d="m12 3 1.8 4.7L18.5 9.5l-4.7 1.8L12 16l-1.8-4.7L5.5 9.5l4.7-1.8z"/><path d="M18.5 15.5 19.4 18l2.5.9-2.5.9-.9 2.5-.9-2.5L15 18l2.6-.9z"/>',
    "pill": '<rect x="3" y="8.5" width="18" height="7" rx="3.5" transform="rotate(-45 12 12)"/><path d="m9 9 6 6"/>',
    "atom": '<circle cx="12" cy="12" r="1.6"/><ellipse cx="12" cy="12" rx="9" ry="4" /><ellipse cx="12" cy="12" rx="9" ry="4" transform="rotate(60 12 12)"/><ellipse cx="12" cy="12" rx="9" ry="4" transform="rotate(120 12 12)"/>',
    "leaf": '<path d="M4.5 19.5c0-8 5-14 15-14 0 10-5.5 14-11 14a4 4 0 0 1-4 0z"/><path d="M9 15c1.8-3 4.4-5.2 7.5-6.5"/>',
    "activity": '<path d="M3 12h4l2.5-7 5 14L17 12h4"/>',
    "dumbbell": '<path d="M6.5 6.5v11"/><path d="M3.5 9v5"/><path d="M17.5 6.5v11"/><path d="M20.5 9v5"/><path d="M6.5 12h11"/>',
    "smile": '<circle cx="12" cy="12" r="9"/><path d="M8.5 14.2a4.5 4.5 0 0 0 7 0"/><path d="M9 9.5h.01"/><path d="M15 9.5h.01"/>',
    "sun": '<circle cx="12" cy="12" r="4"/><path d="M12 2.5v2"/><path d="M12 19.5v2"/><path d="M2.5 12h2"/><path d="M19.5 12h2"/><path d="m5.2 5.2 1.4 1.4"/><path d="m17.4 17.4 1.4 1.4"/><path d="m18.8 5.2-1.4 1.4"/><path d="m6.6 17.4-1.4 1.4"/>',
    "scale": '<path d="M12 3v18"/><path d="M7 21h10"/><path d="M4.5 8 12 5.5 19.5 8"/><path d="M4.5 8 2 14a3.5 3.5 0 0 0 5 0z"/><path d="M19.5 8 17 14a3.5 3.5 0 0 0 5 0z"/>',
    "home": '<path d="m3.5 10.5 8.5-7 8.5 7"/><path d="M6 9.5V20h12V9.5"/><path d="M10 20v-5.5h4V20"/>',
    "message-circle": '<path d="M20.5 11.6a8.1 8.1 0 0 1-8.7 8.1 8.4 8.4 0 0 1-3.2-.8L3.5 20.5l1.6-5.1a8.4 8.4 0 0 1-.8-3.2 8.1 8.1 0 0 1 8.1-8.7 8.1 8.1 0 0 1 8.1 8.1z"/>',
    "facebook": '<path d="M15.5 3H13a4 4 0 0 0-4 4v3H6.5v4H9v7h4v-7h3l.5-4H13V7.5a1 1 0 0 1 1-1h1.5z"/>',
    "instagram": '<rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><path d="M17.5 6.5h.01"/>',
    "alert-circle": '<circle cx="12" cy="12" r="9"/><path d="M12 8v4.5"/><path d="M12 16h.01"/>',
    "loader": '<path d="M12 3v3"/><path d="M12 18v3"/><path d="M5.6 5.6l2.1 2.1"/><path d="M16.3 16.3l2.1 2.1"/><path d="M3 12h3"/><path d="M18 12h3"/><path d="m5.6 18.4 2.1-2.1"/><path d="m16.3 7.7 2.1-2.1"/>',
    "award": '<circle cx="12" cy="9" r="5.5"/><path d="m8.5 13.5-1 7.5 4.5-2.5 4.5 2.5-1-7.5"/>',
    "sofa": '<path d="M4 11V8.5A2.5 2.5 0 0 1 6.5 6h11A2.5 2.5 0 0 1 20 8.5V11"/><path d="M3 11.5a2 2 0 0 1 2 2V16h14v-2.5a2 2 0 1 1 4 0V19H1v-5.5a2 2 0 0 1 2-2z" /><path d="M7 16v-4h10v4"/>',
    "syringe": '<path d="m17 3 4 4"/><path d="m15 5 4 4"/><path d="M13.5 6.5 6 14v4h4l7.5-7.5z"/><path d="m9 13 2 2"/><path d="M6 18l-3 3"/>',
    "wallet": '<path d="M3 7.5A2.5 2.5 0 0 1 5.5 5H18a1 1 0 0 1 1 1v2"/><rect x="3" y="8" width="18" height="11" rx="2.5"/><path d="M16.5 13.5h.01"/>',
    "users": '<circle cx="9" cy="8" r="3.4"/><path d="M15.5 20v-1.6a3.4 3.4 0 0 0-3.4-3.4H6.9a3.4 3.4 0 0 0-3.4 3.4V20"/><path d="M16.5 4.8a3.4 3.4 0 0 1 0 6.4"/><path d="M20.5 20v-1.6a3.4 3.4 0 0 0-2.5-3.3"/>',
    "building": '<rect x="5" y="3" width="14" height="18" rx="1.5"/><path d="M9 7h2"/><path d="M13 7h2"/><path d="M9 11h2"/><path d="M13 11h2"/><path d="M10.5 21v-4h3v4"/>',
    "plane": '<path d="M10.5 20.5 12 15l7.5-2.2a2 2 0 0 0-.6-3.9L13 9.9 9.5 3.5 7.6 4l1.6 6.5-4.1 1.2-2-2.3-1.4.4 2 3.9-1 3.4 1.4.4 2.3-2.6 4.1-1.2-.6 6.6z"/>',
    "thermometer": '<path d="M13.5 14.2V5.5a2 2 0 1 0-4 0v8.7a4 4 0 1 0 4 0z"/>',
}


# ==========================================================================
#  SERVICES  (17 — no individual pages, all presented as cards)
# ==========================================================================
SERVICES = [
    dict(name="Hangover IV Therapy", icon="citrus", cat="recovery",
         desc="Rehydrate fast and calm the nausea, headache and brain fog that follow a big night out.",
         tags=["Fluids &amp; electrolytes", "Anti-nausea", "B-complex", "Vitamin B12"],
         time="45–60 min", best="Mornings after, weddings, bachelor &amp; bachelorette weekends"),
    dict(name="Migraine IV Therapy", icon="brain", cat="recovery",
         desc="Targeted relief for migraine and tension headaches, delivered in a quiet, dimly lit room at home.",
         tags=["Magnesium", "Anti-inflammatory", "Anti-nausea", "B-complex"],
         time="45–60 min", best="Chronic migraine sufferers, screen fatigue, weather triggers"),
    dict(name="Immune Boost IV Therapy", icon="shield-check", cat="immunity",
         desc="A high-dose vitamin and mineral blend to support your immune system before or during illness.",
         tags=["Vitamin C", "Zinc", "B-complex", "Glutathione"],
         time="45–60 min", best="Cold and flu season, pre-travel, back-to-school weeks"),
    dict(name="Dehydration IV Therapy", icon="droplet", cat="recovery wellness",
         desc="Straight, fast rehydration for Florida heat, long shifts, stomach bugs and outdoor days.",
         tags=["Balanced electrolytes", "Sterile fluids", "Optional add-ons"],
         time="30–45 min", best="Heat exhaustion, theme park days, illness recovery"),
    dict(name="Fatigue IV Therapy", icon="battery-low", cat="energy",
         desc="For the tiredness that sleep does not fix — replenishes the nutrients energy production depends on.",
         tags=["B12", "B-complex", "Magnesium", "Amino blend"],
         time="45–60 min", best="Burnout, shift work, new parents, long project sprints"),
    dict(name="Energy Boost IV Therapy", icon="zap", cat="energy",
         desc="A clean lift without the crash of caffeine or energy drinks, absorbed directly into your bloodstream.",
         tags=["B12", "B-complex", "Taurine", "Amino acids"],
         time="30–45 min", best="Big presentation days, travel, early mornings"),
    dict(name="NAD+ IV Therapy", icon="dna", cat="energy wellness",
         desc="A slow, deliberate infusion of NAD+, a coenzyme involved in cellular energy and repair.",
         tags=["NAD+", "Slow-drip protocol", "Optional B-complex"],
         time="90–180 min", best="Cellular wellness, mental clarity, longevity routines"),
    dict(name="Vitamin C IV Therapy", icon="citrus", cat="immunity",
         desc="High-dose vitamin C at levels the gut simply cannot absorb from tablets or food.",
         tags=["High-dose vitamin C", "Fluids", "Optional zinc"],
         time="45–75 min", best="Immune support, seasonal illness, general wellness"),
    dict(name="Glutathione IV Therapy", icon="sparkles", cat="beauty immunity",
         desc="The body's master antioxidant, used to support detox pathways, skin brightness and cellular defence.",
         tags=["Glutathione", "Vitamin C", "Fluids"],
         time="30–45 min", best="Skin tone and clarity, detox support, oxidative stress"),
    dict(name="B12 IV Therapy", icon="pill", cat="energy",
         desc="A focused B12 top-up for energy, mood and nerve health — especially useful on plant-based diets.",
         tags=["Methylcobalamin B12", "Fluids", "Optional B-complex"],
         time="30–40 min", best="Low energy, vegan and vegetarian diets, low mood"),
    dict(name="Amino Acid IV Therapy", icon="atom", cat="energy",
         desc="Essential amino acids to support muscle repair, metabolism and lean tissue maintenance.",
         tags=["Amino blend", "B-complex", "Fluids"],
         time="45–60 min", best="Training blocks, metabolic support, recovery weeks"),
    dict(name="Antioxidant IV Therapy", icon="leaf", cat="wellness immunity",
         desc="A protective blend that helps your body manage the oxidative stress of modern life.",
         tags=["Glutathione", "Vitamin C", "Zinc", "Selenium"],
         time="45–60 min", best="High-stress periods, city living, poor sleep"),
    dict(name="Recovery IV Therapy", icon="heart", cat="recovery",
         desc="A broad restore-and-repair drip for the days after illness, travel, surgery or a heavy week.",
         tags=["Fluids", "B-complex", "Magnesium", "Vitamin C"],
         time="45–60 min", best="Post-illness, post-travel, post-event recovery"),
    dict(name="Athletic Recovery IV Therapy", icon="dumbbell", cat="energy",
         desc="Built for training loads — replaces what you sweat out and supports faster muscle turnaround.",
         tags=["Electrolytes", "Amino acids", "Magnesium", "B-complex"],
         time="45–60 min", best="Race days, marathons, triathlons, tournament weekends"),
    dict(name="Beauty IV Therapy", icon="smile", cat="beauty",
         desc="Hydration plus beauty-supporting nutrients for skin, hair and nails from the inside out.",
         tags=["Biotin", "Vitamin C", "Glutathione", "B-complex"],
         time="45–60 min", best="Weddings, photoshoots, milestone events"),
    dict(name="Skin Glow IV Therapy", icon="sun", cat="beauty",
         desc="A brightening blend focused on radiance, tone and hydration for tired, dull-looking skin.",
         tags=["Glutathione", "Vitamin C", "Hydration blend"],
         time="30–45 min", best="Dull skin, sun exposure, pre-event glow"),
    dict(name="Weight Loss IV Therapy", icon="scale", cat="wellness",
         desc="A metabolic support drip designed to work alongside a supervised weight management plan.",
         tags=["Lipotropic blend", "B12", "L-carnitine", "Amino acids"],
         time="45–60 min", best="Structured programs, plateau support, metabolic health",
         note="Available only as part of a supervised program, after medical review."),
]

FILTERS = [
    ("all", "All therapies"),
    ("recovery", "Recovery &amp; relief"),
    ("energy", "Energy &amp; performance"),
    ("immunity", "Immunity"),
    ("beauty", "Beauty &amp; skin"),
    ("wellness", "Everyday wellness"),
]


# ==========================================================================
#  LOCATIONS  (no addresses, no maps, no directions, no coordinates)
# ==========================================================================
LOCATIONS = [
    dict(
        slug="dr-phillips", name="Dr. Phillips", short="Dr. Phillips",
        img="location-dr-phillips.jpg",
        blurb="Concierge IV therapy for Dr. Phillips homes, private clubs and Restaurant Row hotels.",
        intro=("Dr. Phillips runs at a different pace — long lunches on Restaurant Row, early tee times, "
               "back-to-back client dinners and a calendar that rarely slows down. Orlando IV Care brings "
               "the whole treatment to you, so recovering from a heavy week never costs you a morning."),
        why=[("Restaurant Row recovery", "Late dinners and wine pairings are part of the routine here. A morning-after drip gets you back to work without writing off the day."),
             ("Golf and club days", "Long rounds in Florida humidity drain you faster than you notice. We hydrate you before or after, at home."),
             ("Executive schedules", "Appointments booked around your calendar, including early mornings and evenings, with no waiting room in between."),
             ("Private and discreet", "Your nurse arrives in plain clothing with everything packed away. Neighbours see a visitor, not a clinic.")],
        popular=["Hangover IV Therapy", "NAD+ IV Therapy", "Beauty IV Therapy", "Immune Boost IV Therapy", "Energy Boost IV Therapy", "Glutathione IV Therapy"],
        testimonials=[
            ("Booked at 8am after a work dinner and had a nurse at my door before 10. I made my 11 o'clock call feeling human again.", "Jessica R.", "Dr. Phillips"),
            ("We do a group drip before every charity golf day now. Easily the best money our foursome spends.", "Andrew M.", "Dr. Phillips"),
            ("Professional, quiet, and completely discreet. She was in and out and my afternoon was untouched.", "Priya N.", "Dr. Phillips"),
        ],
        faqs=[
            ("How quickly can you get to Dr. Phillips?", "Same-day appointments are usually available, and we often reach Dr. Phillips within a couple of hours of your request. Booking the night before guarantees your preferred window."),
            ("Can you treat me at a hotel or private club?", "Yes. We regularly treat guests in hotels, resorts and private residences across the Dr. Phillips area, as long as we have permission to be on site and a comfortable place for you to sit."),
            ("Do you handle groups?", "We do. Bachelor and bachelorette parties, golf groups, corporate retreats and family gatherings are all common. Let us know your headcount when you book so we can send the right number of nurses."),
            ("Is there a call-out fee for Dr. Phillips?", "Travel within our core Orlando service area is included in the treatment price. If you are outside it, we will tell you before you confirm — never after."),
            ("Who actually administers the IV?", "A licensed registered nurse, working under physician-approved protocols. Your nurse reviews your health history before starting and stays with you for the entire treatment."),
        ],
    ),
    dict(
        slug="lake-nona", name="Lake Nona", short="Lake Nona",
        img="location-lake-nona.jpg",
        blurb="Mobile IV therapy for Lake Nona homes, offices and training facilities.",
        intro=("Lake Nona is built around health — medical campuses, performance facilities, running trails and "
               "a community that takes recovery seriously. Orlando IV Care fits that mindset: clinically sound "
               "treatments, delivered at home so your training, work and family time stay intact."),
        why=[("Performance-minded community", "Runners, cyclists, triathletes and weekend athletes use hydration and amino drips to shorten the gap between sessions."),
             ("Long work-from-home days", "Screen fatigue, skipped lunches and dehydration add up. A mid-week drip resets you without leaving your desk for long."),
             ("Young families", "When a stomach bug moves through the house, we come to you instead of asking you to sit in a waiting room with a sick child."),
             ("Clinically grounded care", "You live in a neighbourhood that knows healthcare. Our protocols, sourcing and nurse credentials are built to stand up to that scrutiny.")],
        popular=["Athletic Recovery IV Therapy", "Dehydration IV Therapy", "Energy Boost IV Therapy", "Amino Acid IV Therapy", "Immune Boost IV Therapy", "Fatigue IV Therapy"],
        testimonials=[
            ("I book the athletic recovery drip the evening after long runs. My legs are noticeably better the next morning.", "Marcus T.", "Lake Nona"),
            ("Our whole family had the flu. They came out twice in one week and were kind to my kids both times.", "Danielle S.", "Lake Nona"),
            ("As someone who works in healthcare, I asked a lot of questions. Every answer was straight and well informed.", "Dr. Aaron K.", "Lake Nona"),
        ],
        faqs=[
            ("Can you come to my office in Lake Nona?", "Yes, as long as your employer approves it and there is a private, comfortable space to sit for the treatment. Corporate wellness sessions for teams are also available."),
            ("Is IV therapy useful before a race?", "Many athletes hydrate the day before an event rather than the morning of. Your nurse will talk through timing with you, and if a drip is not appropriate for your event, we will say so."),
            ("How long does an appointment take?", "Most treatments run 30–60 minutes from arrival to clean-up. NAD+ is slower by design and can take up to three hours."),
            ("Can I be treated during pregnancy?", "Only with clearance from your OB or physician. Bring that clearance to the appointment and we will review it with you before starting."),
            ("Do you offer memberships?", "We do. Regular clients on monthly plans pay less per treatment and get priority booking windows. Ask us when you book."),
        ],
    ),
    dict(
        slug="winter-park", name="Winter Park", short="Winter Park",
        img="location-winter-park.jpg",
        blurb="At-home IV therapy for Winter Park residences, boutique hotels and Park Avenue businesses.",
        intro=("Winter Park has its own rhythm — brick streets, tree-lined avenues and a preference for things "
               "done properly. Orlando IV Care matches it. Registered nurses, unhurried appointments and "
               "treatments delivered in your own home rather than a clinic under fluorescent lights."),
        why=[("A quieter kind of care", "No waiting rooms, no forms on a clipboard. You sit in your own chair and someone qualified takes care of the rest."),
             ("Boutique hotels and guests", "Visitors staying near Park Avenue often book on arrival to shake off travel fatigue before a weekend of walking and dining."),
             ("Event and wedding season", "Rehearsal dinners, receptions and photo days — beauty and hydration drips are a standing part of many Winter Park weekends."),
             ("Longstanding routines", "Many Winter Park clients book the same treatment on the same weekday each month. We keep your history so nothing needs re-explaining.")],
        popular=["Beauty IV Therapy", "Skin Glow IV Therapy", "Migraine IV Therapy", "Immune Boost IV Therapy", "Recovery IV Therapy", "Vitamin C IV Therapy"],
        testimonials=[
            ("I get terrible migraines and driving to a clinic is the last thing I can do. They came to me and dimmed the lights without being asked.", "Amanda L.", "Winter Park"),
            ("Booked beauty drips for the bridal party the morning of the wedding. Everyone looked and felt incredible in the photos.", "Sophie D.", "Winter Park"),
            ("Same nurse every month, remembers my history, always on time. That consistency is why I stay.", "Robert H.", "Winter Park"),
        ],
        faqs=[
            ("Do you treat guests staying in Winter Park hotels?", "Yes. We treat visitors in hotels, short-term rentals and guest houses regularly. Just make sure the property allows visitors to your room."),
            ("Can you do a group before a wedding?", "Absolutely. Bridal parties are one of our most common group bookings. Give us your headcount and timing and we will schedule enough nurses to finish comfortably before hair and makeup."),
            ("Does it hurt?", "You will feel a brief pinch when the catheter goes in, then nothing more than the cuff pressure. Our nurses place IVs daily and are quick about it."),
            ("What if I have small veins?", "Tell us when you book. Your nurse will bring smaller gauge equipment and take extra time with warming and positioning."),
            ("Can I cancel or reschedule?", "Yes — just give us as much notice as you can so we can offer the slot to someone else. There is no charge for reasonable notice."),
        ],
    ),
    dict(
        slug="windermere", name="Windermere", short="Windermere",
        img="location-windermere.jpg",
        blurb="Private, at-home IV therapy for Windermere estates and lakefront communities.",
        intro=("Windermere is quiet by design, and most of our clients here want their wellness routine to be "
               "the same. Orlando IV Care brings the full treatment to your home — gated communities included — "
               "with a licensed nurse, sterile supplies and no trace left behind."),
        why=[("Gated community access", "Give us your gate instructions when you book and your nurse will arrive without a string of calls from the guard house."),
             ("Lake days and boat weekends", "Sun, salt and a long day on the water dehydrate you fast. An evening drip means Sunday is not a write-off."),
             ("Family wellness routines", "Parents, teens over 18 and visiting relatives often book together. One visit, several treatments, no travel."),
             ("Total privacy", "No signage, no branded vehicles at the door and nothing left in your bin. Discretion is part of the service.")],
        popular=["Immune Boost IV Therapy", "Dehydration IV Therapy", "NAD+ IV Therapy", "Recovery IV Therapy", "Antioxidant IV Therapy", "Energy Boost IV Therapy"],
        testimonials=[
            ("After a full day on the boat we all felt awful. They came out at 7pm and treated four of us in the kitchen. Life-saving.", "Chris B.", "Windermere"),
            ("The nurse handled the gate, the paperwork and my nervous questions without missing a beat.", "Maria G.", "Windermere"),
            ("We book immune drips for the whole family before every trip now. It has become a routine.", "Thomas W.", "Windermere"),
        ],
        faqs=[
            ("How does gate access work?", "Add your community name and gate instructions in the booking notes, or call the guard house ahead. Your nurse will call you on arrival if there is any hold-up."),
            ("Can several people be treated in one visit?", "Yes. Group bookings at a single address are straightforward and often the easiest way to schedule. Tell us how many people so we send enough staff and supplies."),
            ("Do you come out in the evening?", "We do. Evening appointments are popular in Windermere, especially after weekends on the water. Availability is best when you book at least a day ahead."),
            ("What do I need to have ready?", "A comfortable chair or sofa, somewhere to rest your arm and about an hour of your time. We bring everything else, including a sharps container."),
            ("Are treatments safe for older adults?", "Often, yes, but it depends on the person. Your nurse reviews medical history, medications and kidney and heart conditions before treating anyone, and will decline if a drip is not appropriate."),
        ],
    ),
    dict(
        slug="celebration", name="Celebration", short="Celebration",
        img="location-celebration.jpg",
        blurb="Mobile IV therapy for Celebration homes, resorts and vacation rentals near the parks.",
        intro=("Celebration sits at the edge of the busiest holiday destination in the country, and that shows "
               "up in how people feel. Twelve-hour park days, Florida heat, time-zone changes and very little "
               "sleep. Orlando IV Care rehydrates you where you are staying, so the rest of the trip is not lost."),
        why=[("Theme park recovery", "Twenty thousand steps in ninety-degree heat is a genuine physical event. Fluids and electrolytes get families back on their feet."),
             ("Vacation rentals and resorts", "We treat guests in rentals, resorts and hotels around Celebration daily — most bookings come from people mid-trip."),
             ("Jet lag and travel fatigue", "Long-haul arrivals, red-eye flights and dry cabin air leave you flat. A drip on arrival day shortens the adjustment."),
             ("Families travelling together", "Multi-generational trips mean somebody is always run down. We can treat several adults in one visit at the same address.")],
        popular=["Dehydration IV Therapy", "Hangover IV Therapy", "Energy Boost IV Therapy", "Immune Boost IV Therapy", "Recovery IV Therapy", "Fatigue IV Therapy"],
        testimonials=[
            ("Day three of our trip and we were wrecked. One drip each and we made it through the rest of the week.", "Karen P.", "Celebration"),
            ("Flew in from London, felt terrible, booked that afternoon. Best decision of the holiday.", "James F.", "Celebration"),
            ("They treated my husband and me in our rental while the kids napped. Unbelievably convenient.", "Nicole A.", "Celebration"),
        ],
        faqs=[
            ("Can you treat me at a resort or vacation rental?", "Yes, this is most of what we do in Celebration. Confirm your property allows visitors, and have your unit or room number ready when you book."),
            ("How fast can you get to me?", "Same-day appointments are common. During peak holiday weeks we fill up early, so booking the night before is the safest way to lock in a time."),
            ("Is IV therapy good for heat exhaustion?", "Rehydration helps with mild heat-related fatigue, and that is a large part of what we treat here. Serious heat stroke is a medical emergency — call 911 and do not wait for us."),
            ("Can children be treated?", "We treat adults aged 18 and over only. For children, please contact a paediatric urgent care provider."),
            ("What payment methods do you take?", "All major credit cards, plus HSA and FSA cards where your plan allows it. Payment is taken at the appointment, not in advance."),
        ],
    ),
]

STEPS = [
    ("Book", "calendar", "Choose your therapy, location and time. Same-day appointments are usually available."),
    ("We come to you", "car", "Your licensed nurse arrives with everything needed — no clinic, no waiting room."),
    ("Relax &amp; rehydrate", "sofa", "Sit back for 30–60 minutes while your treatment is delivered and monitored."),
    ("Feel the difference", "heart", "Most people feel noticeably better before the nurse has packed up."),
]

WHY_POINTS = [
    "Medical-grade ingredients",
    "Customised treatments",
    "Licensed, experienced nurses",
    "Safe, clean and professional",
    "Mobile service — we come to you",
    "Transparent, all-in pricing",
]


# ==========================================================================
#  SHARED HTML COMPONENTS
# ==========================================================================
# ==========================================================================
#  PHOTOGRAPHY
#  --------------------------------------------------------------------------
#  Real free stock photos from Unsplash (Unsplash Licence — free for commercial
#  use, no attribution required). They are hot-linked from Unsplash's CDN, which
#  Unsplash explicitly supports, so nothing needs downloading.
#
#  To use your OWN photo instead:
#     1. put it in /images  (e.g. images/hero-iv-therapy.jpg)
#     2. run:  python3 _tools/use-local-images.py
#  That rewrites every <img> to point at /images/<filename> in one pass.
#  The filename to use for each slot is the dict key below.
# ==========================================================================
PHOTOS = {
    "hero-iv-therapy.jpg":        "photo-1516574187841-cb9cc2ca948b",
    "services-hero.jpg":          "photo-1583830379747-195159d0de82",
    "locations-hero.jpg":         "photo-1609184889233-eff6dd93def4",
    "about-hero.jpg":             "photo-1736289162890-78f1ff4f8bd3",
    "contact-hero.jpg":           "photo-1667584523543-d1d9cc828a15",
    "location-dr-phillips.jpg":   "photo-1756435292384-1bf32eff7baf",
    "location-lake-nona.jpg":     "photo-1706808849780-7a04fbac83ef",
    "location-winter-park.jpg":   "photo-1785632662559-2fd11a69f4ff",
    "location-windermere.jpg":    "photo-1759020623226-73ec7a068b11",
    "location-celebration.jpg":   "photo-1759751588192-ac038edbd429",
    "why-choose-iv-care.jpg":     "photo-1589295926521-49b366c49767",
    "about-team.jpg":             "photo-1691139601099-932c01ec198b",
    "about-nurse.jpg":            "photo-1631815590016-ebce183022ce",
    "iv-drip-detail.jpg":         "photo-1585960691786-a593e76d3847",
    "mobile-service.jpg":         "photo-1758691462321-9b6c98c40f7e",
    "standards.jpg":              "photo-1635506729176-f18c7a773f8e",
    "testimonial-1.jpg":          "photo-1494790108377-be9c29b29330",
    "testimonial-2.jpg":          "photo-1507003211169-0a1dd7228f2d",
    "testimonial-3.jpg":          "photo-1580489944761-15a19d654956",
}

# Flip to True (or run _tools/use-local-images.py) to serve from /images instead.
USE_LOCAL_IMAGES = False


def photo_url(name, w, h):
    if USE_LOCAL_IMAGES or name not in PHOTOS:
        return "{{P}}images/" + name
    return ("https://images.unsplash.com/%s?auto=format&fit=crop&w=%d&h=%d&q=80"
            % (PHOTOS[name], w, h))


def img(name, alt, w, h, cls="", eager=False, sizes=None):
    attrs = 'class="%s" ' % cls if cls else ""
    load = 'loading="eager" fetchpriority="high"' if eager else 'loading="lazy"'
    sz = ' sizes="%s"' % sizes if sizes else ""
    return ('<img %ssrc="%s" data-image-name="%s" alt="%s" width="%d" height="%d" %s decoding="async"%s>') % (
        attrs, photo_url(name, w, h), name, alt, w, h, load, sz)


def nav_html(active):
    def cur(key):
        return ' aria-current="page"' if active == key else ''

    loc_items = "".join(
        '<li><a href="{{P}}locations/%s.html">%s</a></li>' % (l["slug"], l["name"]) for l in LOCATIONS
    )

    return """
      <nav class="nav" id="primary-nav" aria-label="Main">
        <div class="nav__head">
          <span class="nav__head-title">Menu</span>
          <button class="nav__close" type="button" aria-label="Close menu">%s</button>
        </div>

        <a class="nav__link" href="{{P}}index.html"%s>Home</a>
        <a class="nav__link" href="{{P}}services.html"%s>Services</a>
        <div class="nav__item">
          <button class="nav__link nav__toggle" type="button" aria-expanded="false" aria-haspopup="true">
            <span>Locations</span> %s
          </button>
          <ul class="nav__menu">
            <li><a href="{{P}}locations.html">All locations</a></li>
            %s
          </ul>
        </div>
        <a class="nav__link" href="{{P}}about.html"%s>About Us</a>
        <a class="nav__link" href="{{P}}contact.html"%s>Contact</a>

        <a class="btn btn--sm nav__cta" href="{{P}}contact.html#book">Book Now %s</a>

        <div class="nav__extra">
          <a href="tel:%s">%s <span>%s</span></a>
          <a href="mailto:%s">%s <span>%s</span></a>
          <p>%s</p>
        </div>
      </nav>""" % (
        icon("x", 20),
        cur("home"), cur("services"),
        icon("chevron-down", 16, "nav__caret"),
        loc_items,
        cur("about"), cur("contact"),
        icon("arrow-right", 16, "btn__icon"),
        SITE["phone_href"], icon("phone", 18), SITE["phone_display"],
        SITE["email"], icon("mail", 18), SITE["email"],
        SITE["hours"],
    )


def logo_mark(uid):
    """Gradient ids must stay unique — the logo appears three times per page."""
    return """<svg class="logo__mark" viewBox="0 0 34 40" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" focusable="false">
        <path d="M17 1.5C17 1.5 2.5 17.4 2.5 25.6A14.5 14.5 0 0 0 17 40a14.5 14.5 0 0 0 14.5-14.4C31.5 17.4 17 1.5 17 1.5Z" fill="url(#%s)"/>
        <path d="M17 9.5c0 4.3-5.2 7.6-5.2 12.4A5.2 5.2 0 0 0 17 27a5.2 5.2 0 0 0 5.2-5.1c0-4.8-5.2-8.1-5.2-12.4Z" fill="#F6FEFD" opacity=".85"/>
        <defs><linearGradient id="%s" x1="2.5" y1="1.5" x2="31.5" y2="40" gradientUnits="userSpaceOnUse">
          <stop stop-color="#5FE0D5"/><stop offset="1" stop-color="#0A7C75"/></linearGradient></defs>
      </svg>""" % (uid, uid)


def logo(extra="", uid="logo-grad"):
    return """<a class="logo %s" href="{{P}}index.html" aria-label="%s — home">
        %s
        <span class="logo__text"><span class="logo__top">ORLANDO</span><span class="logo__bottom">IV CARE</span></span>
      </a>""" % (extra, SITE["name"], logo_mark(uid))


def header_html(active):
    return """
  <a class="skip-link" href="#main">Skip to main content</a>
  <header class="site-header">
    <div class="nav-scrim" aria-hidden="true"></div>
    <div class="container site-header__inner">
      %s
      %s
      <div class="header__actions">
        <button class="nav-toggle" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="primary-nav">
          <span class="nav-toggle__bar"></span><span class="nav-toggle__bar"></span><span class="nav-toggle__bar"></span>
        </button>
      </div>
    </div>
  </header>""" % (logo(uid="logo-grad-header"), nav_html(active))


def cta_band():
    return """
  <section class="cta-band">
    <div class="container cta-band__inner">
      <div class="cta-band__brand">
        %s
      </div>
      <div>
        <h2>Ready to Feel Your Best?</h2>
        <p>Book your IV therapy today and experience the %s difference.</p>
      </div>
      <div class="cta-band__actions">
        <a class="btn btn--light btn--lg" href="{{P}}contact.html#book">Book Now %s</a>
        <a class="btn btn--outline-light btn--lg" href="tel:%s">%s Call us</a>
      </div>
    </div>
  </section>""" % (logo("logo--footer", "logo-grad-cta"), SITE["name"], icon("arrow-right", 18, "btn__icon"),
                   SITE["phone_href"], icon("phone", 18))


def footer_html():
    loc_links = "".join('<li><a href="{{P}}locations/%s.html">%s</a></li>' % (l["slug"], l["name"]) for l in LOCATIONS)
    return """
  <footer class="site-footer">
    <div class="container">
      <div class="site-footer__top">
        <div>
          %s
          <p style="margin-top:1rem;max-width:34ch">Premium mobile IV therapy delivered to homes, offices, hotels and rentals across Orlando and the surrounding communities.</p>
          <div class="social-row">
            <a class="social-btn" href="%s" aria-label="%s on Facebook" rel="noopener">%s</a>
            <a class="social-btn" href="%s" aria-label="%s on Instagram" rel="noopener">%s</a>
            <a class="social-btn" href="tel:%s" aria-label="Call %s">%s</a>
          </div>
        </div>
        <div>
          <h4>Explore</h4>
          <ul class="footer-links">
            <li><a href="{{P}}index.html">Home</a></li>
            <li><a href="{{P}}services.html">Services</a></li>
            <li><a href="{{P}}locations.html">Locations</a></li>
            <li><a href="{{P}}about.html">About Us</a></li>
            <li><a href="{{P}}contact.html">Contact</a></li>
          </ul>
        </div>
        <div>
          <h4>Locations</h4>
          <ul class="footer-links">%s</ul>
        </div>
        <div>
          <h4>Get in touch</h4>
          <ul class="footer-links">
            <li><a href="tel:%s">%s</a></li>
            <li><a href="mailto:%s">%s</a></li>
          </ul>
          <p style="margin-top:1rem">%s<br>Serving Orlando &amp; surrounding areas</p>
          <a class="btn btn--sm" style="margin-top:1rem" href="{{P}}contact.html#book">Book Your IV Therapy %s</a>
        </div>
      </div>

      <p class="disclaimer">
        <strong>Medical disclaimer.</strong> If you think you may have a medical emergency, call 911 immediately.
        This website is for general information only and is not medical advice, diagnosis or treatment. IV therapy
        is not a substitute for care from your physician, and statements on this site have not been evaluated by
        the Food and Drug Administration. All treatments are subject to a nurse assessment and may be declined
        where they are not clinically appropriate. Always consult your physician before beginning any new therapy.
        Services are available to adults aged 18 and over.
      </p>

      <div class="site-footer__bottom">
        <p>&copy; <span data-year>2026</span> %s. All rights reserved.</p>
        <p>Licensed registered nurses &middot; Physician-approved protocols &middot; HSA/FSA friendly</p>
      </div>
    </div>
  </footer>

  <div class="mobile-bar">
    <a class="btn btn--ghost" style="background:rgba(255,255,255,.06);color:#fff;border-color:rgba(255,255,255,.25)" href="tel:%s">%s Call</a>
    <a class="btn" href="{{P}}contact.html#book">Book Now %s</a>
  </div>

  <script src="{{P}}js/main.js" defer></script>
</body>
</html>
""" % (
        logo("logo--footer", "logo-grad-footer"),
        SITE["facebook"], SITE["name"], icon("facebook", 20),
        SITE["instagram"], SITE["name"], icon("instagram", 20),
        SITE["phone_href"], SITE["name"], icon("phone", 20),
        loc_links,
        SITE["phone_href"], SITE["phone_display"],
        SITE["email"], SITE["email"],
        SITE["hours"],
        icon("arrow-right", 16, "btn__icon"),
        SITE["name"],
        SITE["phone_href"], icon("phone", 18), icon("arrow-right", 16, "btn__icon"),
    )


def head_html(title, description, canonical, schema=None, og_image="hero-iv-therapy.jpg"):
    ld = ""
    if schema:
        ld = '\n  <script type="application/ld+json">%s</script>' % json.dumps(schema, indent=2)
    return """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>%s</title>
  <meta name="description" content="%s">
  <link rel="canonical" href="%s">
  <meta name="theme-color" content="#080C0D">
  <meta name="robots" content="index, follow">

  <meta property="og:type" content="website">
  <meta property="og:site_name" content="%s">
  <meta property="og:title" content="%s">
  <meta property="og:description" content="%s">
  <meta property="og:url" content="%s">
  <meta property="og:image" content="%s/images/%s">
  <meta name="twitter:card" content="summary_large_image">

  <link rel="icon" href="{{P}}images/favicon.svg" type="image/svg+xml">
  <link rel="apple-touch-icon" href="{{P}}images/favicon.svg">

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700&family=Inter:wght@400;500;600&display=swap">
  <link rel="stylesheet" href="{{P}}css/style.css">%s
</head>
<body>
%s
""" % (title, description, canonical, SITE["name"], title, description, canonical,
       SITE["domain"], og_image, ld, EDIT_ME)


def org_schema():
    return {
        "@context": "https://schema.org",
        "@type": "MedicalBusiness",
        "name": SITE["name"],
        "description": "Premium mobile IV therapy delivered to homes, offices, hotels and rentals across Orlando, Florida.",
        "url": SITE["domain"],
        "telephone": SITE["phone_display"],
        "email": SITE["email"],
        "priceRange": "$$",
        "areaServed": [{"@type": "Place", "name": l["name"]} for l in LOCATIONS] + [{"@type": "City", "name": "Orlando"}],
        "medicalSpecialty": "PreventiveMedicine",
        "availableService": [{"@type": "MedicalTherapy", "name": s["name"]} for s in SERVICES],
    }


def faq_schema(faqs):
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": html.unescape(q),
             "acceptedAnswer": {"@type": "Answer", "text": html.unescape(a)}}
            for q, a in faqs
        ],
    }


def steps_html():
    out = []
    for i, (title, ic, desc) in enumerate(STEPS, start=1):
        out.append("""
        <li class="step reveal" data-delay="%d">
          <span class="step__num" aria-hidden="true">%d</span>
          <span class="step__icon">%s</span>
          <h3>%s</h3>
          <p>%s</p>
        </li>""" % (min(i, 4), i, icon(ic, 30), title, desc))
    return '<ol class="steps">%s</ol>' % "".join(out)


def check_list(points, light=False):
    cls = "check-list check-list--light" if light else "check-list"
    items = "".join('<li>%s<span>%s</span></li>' % (icon("check-circle", 20), p) for p in points)
    return '<ul class="%s">%s</ul>' % (cls, items)


def stars(n=5):
    return '<div class="testi__stars" role="img" aria-label="%d out of 5 stars">%s</div>' % (n, icon("star", 16) * n)


def testimonials_html(items, avatar_prefix="testimonial"):
    out = []
    for i, (quote, name, place) in enumerate(items, start=1):
        av = "%s-%d.jpg" % (avatar_prefix, ((i - 1) % 3) + 1)
        out.append("""
      <figure class="testi reveal" data-delay="%d">
        %s
        <blockquote class="testi__quote">&ldquo;%s&rdquo;</blockquote>
        <figcaption class="testi__who">
          %s
          <span>
            <span class="testi__name">%s</span><br>
            <span class="testi__meta">%s</span>
          </span>
        </figcaption>
      </figure>""" % (i, stars(), quote,
                      img(av, "Portrait of %s" % name, 88, 88, cls="testi__avatar"),
                      name, place))
    return '<div class="testi-grid">%s</div>' % "".join(out)


def faq_html(faqs, start_id=1):
    out = []
    for i, (q, a) in enumerate(faqs, start=start_id):
        out.append("""
        <div class="faq__item">
          <h3 style="margin:0">
            <button class="faq__q" type="button" aria-expanded="false" aria-controls="faq-a-%d" id="faq-q-%d">
              <span>%s</span>
              <span class="faq__icon" aria-hidden="true">%s</span>
            </button>
          </h3>
          <div class="faq__a" id="faq-a-%d" role="region" aria-labelledby="faq-q-%d">
            <div><p>%s</p></div>
          </div>
        </div>""" % (i, i, q, icon("plus", 18), i, i, a))
    return '<div class="faq">%s</div>' % "".join(out)


def service_mini_grid(names=None, limit=None):
    items = SERVICES if names is None else [s for s in SERVICES if s["name"] in names]
    if limit:
        items = items[:limit]
    cards = "".join("""
        <a class="svc-mini" href="{{P}}services.html">
          <span class="svc-mini__icon">%s</span>
          <span class="svc-mini__name">%s</span>
        </a>""" % (icon(s["icon"], 30), s["name"].replace(" IV Therapy", "<br>IV Therapy")) for s in items)
    return '<div class="svc-mini-grid">%s</div>' % cards


def service_cards():
    out = []
    for i, s in enumerate(SERVICES):
        tags = "".join('<li class="tag">%s</li>' % t for t in s["tags"])
        note = '<p class="field__help" style="margin-top:.75rem">%s</p>' % s["note"] if s.get("note") else ""
        out.append("""
      <article class="svc-card reveal" data-category="%s" data-delay="%d">
        <span class="svc-card__icon">%s</span>
        <h3>%s</h3>
        <p class="svc-card__desc">%s</p>
        <ul class="svc-card__tags">%s</ul>
        %s
        <div class="svc-card__meta">
          <span>%s %s</span>
          <span>%s Best for: %s</span>
        </div>
      </article>""" % (s["cat"], (i % 4) + 1, icon(s["icon"], 28), s["name"], s["desc"], tags, note,
                       icon("clock", 15), s["time"], icon("user-check", 15), s["best"]))
    return '<div class="svc-grid" data-filter-target>%s</div>' % "".join(out)


def filter_bar():
    chips = "".join('<button class="chip" type="button" data-filter="%s" aria-pressed="%s">%s</button>'
                    % (key, "true" if key == "all" else "false", label) for key, label in FILTERS)
    return '<div class="filter-bar" role="group" aria-label="Filter therapies by category">%s</div>' % chips


# ==========================================================================
#  PAGE BUILDERS
# ==========================================================================
def write(path, content, depth=0):
    prefix = "../" * depth
    content = content.replace("{{P}}", prefix)
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)
    print("  wrote", path)


def build_home():
    loc_cards = "".join("""
          <a class="loc-card" href="{{P}}locations/%s.html">
            %s
            <span class="loc-card__label">%s %s</span>
          </a>""" % (l["slug"], img(l["img"], "Mobile IV therapy in %s, Orlando" % l["name"], 600, 800),
                     l["name"], icon("arrow-right", 18)) for l in LOCATIONS)

    home_testimonials = [
        ("I've tried everything for my migraines. The migraine IV was a genuine game changer — I was functional within the hour.", "Jessica R.", "Lake Nona"),
        ("Best hangover cure ever. I felt better within thirty minutes and made it to my meeting without anyone knowing.", "Mike T.", "Dr. Phillips"),
        ("Super convenient and completely professional. They came to my home and took great care of me from start to finish.", "Amanda L.", "Winter Park"),
    ]

    body = """
  <main id="main">

    <!-- ================= HERO ================= -->
    <section class="hero">
      <div class="hero__media">
        %s
      </div>
      <div class="container">
        <div class="hero__inner">
          <span class="pill">Premium Mobile IV Therapy</span>
          <h1>Feel Better.<span class="accent">Live Better.</span></h1>
          <p class="hero__sub">Personalised IV therapy treatments delivered wherever you are in Orlando — home, office, hotel or rental.</p>

          <div class="hero__trust">
            <div class="trust-item"><span class="trust-item__icon">%s</span>Doctor supervised</div>
            <div class="trust-item"><span class="trust-item__icon">%s</span>Mobile service</div>
            <div class="trust-item"><span class="trust-item__icon">%s</span>Fast &amp; effective</div>
          </div>

          <div class="hero__actions">
            <a class="btn btn--lg" href="{{P}}contact.html#book">Book Your IV Therapy %s</a>
            <a class="btn btn--outline-light btn--lg" href="{{P}}services.html">View All Services %s</a>
          </div>
        </div>
      </div>
    </section>

    <!-- ================= LOCATIONS ================= -->
    <section class="section" aria-labelledby="loc-h">
      <div class="container">
        <div class="section-head section-head--center reveal">
          <span class="eyebrow">Serving Orlando &amp; surrounding areas</span>
          <h2 id="loc-h">Our <span class="text-accent">Locations</span></h2>
          <p>Same-day mobile IV therapy across the communities we know best.</p>
        </div>

        <div class="loc-rail-wrap reveal">
          <div class="loc-rail" tabindex="0" role="group" aria-label="Locations we serve">%s</div>
        </div>

        <div class="center mt-6">
          <a class="btn btn--ghost" href="{{P}}locations.html">View All Locations %s</a>
        </div>
      </div>
    </section>

    <!-- ================= FEATURED SERVICES ================= -->
    <section class="section section--mint" aria-labelledby="svc-h">
      <div class="container">
        <div class="split">
          <div class="reveal">
            <span class="eyebrow">Our IV therapy services</span>
            <h2 id="svc-h">Boost. Rehydrate.<br><span class="text-accent">Recover.</span></h2>
            <p class="lead">Our customised IV therapies are designed to help you feel your best — fast. Whether you are recovering, recharging or optimising your wellness, we have a drip for you.</p>
            <a class="btn mt-5" href="{{P}}services.html">View All Services %s</a>
          </div>
          <div class="reveal" data-delay="2">
            %s
          </div>
        </div>
      </div>
    </section>

    <!-- ================= HOW IT WORKS ================= -->
    <section class="section" id="how-it-works" aria-labelledby="how-h">
      <div class="container">
        <div class="section-head section-head--center reveal">
          <span class="eyebrow">How it works</span>
          <h2 id="how-h">Wellness Made <span class="text-accent">Simple</span></h2>
          <p>Four steps between you and feeling like yourself again.</p>
        </div>
        %s
      </div>
    </section>

    <!-- ================= WHY CHOOSE US ================= -->
    <section class="section why" aria-labelledby="why-h">
      <div class="container">
        <div class="split">
          <div class="why__media reveal">
            %s
          </div>
          <div class="reveal" data-delay="2">
            <span class="eyebrow">Why choose %s?</span>
            <h2 id="why-h">Wellness. Convenience. <span class="text-accent">Results.</span></h2>
            <p>We are committed to providing the highest quality IV therapy with convenience, compassion and care — delivered by nurses who do this every day.</p>
            %s
            <a class="btn" href="{{P}}contact.html#book">Book Your IV Therapy %s</a>
          </div>
        </div>
      </div>
    </section>

    <!-- ================= ABOUT PREVIEW ================= -->
    <section class="section" aria-labelledby="about-h">
      <div class="container">
        <div class="split split--reverse">
          <div class="reveal">
            <span class="eyebrow">About us</span>
            <h2 id="about-h">Local Care, <span class="text-accent">Clinically Delivered</span></h2>
            <p class="lead">%s was built by Orlando clinicians who were tired of watching people lose a whole day to a waiting room for something that takes under an hour.</p>
            <p>Every treatment is administered by a licensed registered nurse, using medical-grade ingredients and physician-approved protocols. We assess before we treat, we explain what we are giving you, and we say no when a drip is not the right answer.</p>
            <a class="link-arrow mt-5" href="{{P}}about.html">Read our story %s</a>
          </div>
          <div class="about__media reveal" data-delay="2">
            %s
            <span class="badge-float">%s Licensed RNs &middot; Physician-led protocols</span>
          </div>
        </div>

        <div class="stats mt-6" style="margin-top:4rem">
          <div class="reveal"><div class="stat__num">5,000+</div><div class="stat__label">Treatments delivered</div></div>
          <div class="reveal" data-delay="1"><div class="stat__num">4.9&#9733;</div><div class="stat__label">Average client rating</div></div>
          <div class="reveal" data-delay="2"><div class="stat__num">60 min</div><div class="stat__label">Typical appointment</div></div>
          <div class="reveal" data-delay="3"><div class="stat__num">7 days</div><div class="stat__label">A week availability</div></div>
        </div>
      </div>
    </section>

    <!-- ================= TESTIMONIALS ================= -->
    <section class="section section--alt" aria-labelledby="testi-h">
      <div class="container">
        <div class="section-head section-head--center reveal">
          <span class="eyebrow">What our clients say</span>
          <h2 id="testi-h">Real People. Real <span class="text-accent">Results.</span></h2>
        </div>
        %s
      </div>
    </section>

    <!-- ================= FINAL CTA ================= -->
    <section class="section section--dark" aria-labelledby="cta-h">
      <div class="container container--narrow cta-center">
        <div class="reveal">
          <span class="eyebrow">Get started today</span>
          <h2 id="cta-h">Your Best Day Starts With <span class="text-accent">One Hour</span></h2>
          <p class="lead">Tell us where you are and when suits you. We will handle the rest — usually the same day.</p>
          <div class="btn-row">
            <a class="btn btn--lg" href="{{P}}contact.html#book">Book Now %s</a>
            <a class="btn btn--outline-light btn--lg" href="tel:%s">%s %s</a>
          </div>
        </div>
      </div>
    </section>

  </main>
""" % (
        img("hero-iv-therapy.jpg", "Client relaxing in a chair while receiving mobile IV therapy at home in Orlando", 1600, 1000, eager=True),
        icon("stethoscope", 20), icon("car", 20), icon("zap", 20),
        icon("arrow-right", 18, "btn__icon"), icon("arrow-right", 18, "btn__icon"),
        loc_cards,
        icon("map-pin", 16, "btn__icon"),
        icon("arrow-right", 18, "btn__icon"),
        service_mini_grid(limit=10),
        steps_html(),
        img("why-choose-iv-care.jpg", "Orlando IV Care mobile treatment kit and IV bag ready for a home visit", 900, 675),
        SITE["name"], check_list(WHY_POINTS), icon("arrow-right", 18, "btn__icon"),
        SITE["name"], icon("arrow-right", 16),
        img("about-team.jpg", "Registered nurse preparing an IV drip for a client at home", 900, 675),
        icon("shield-check", 20),
        testimonials_html(home_testimonials),
        icon("arrow-right", 18, "btn__icon"),
        SITE["phone_href"], icon("phone", 18), SITE["phone_display"],
    )

    page = (head_html(
        "Mobile IV Therapy in Orlando, FL | %s" % SITE["name"],
        "Premium mobile IV therapy delivered to your home, office or hotel across Orlando. Licensed nurses, medical-grade ingredients, same-day appointments. Book now.",
        SITE["domain"] + "/",
        schema=org_schema())
        + header_html("home") + body + cta_band() + footer_html())
    write("index.html", page, 0)


def build_services():
    faqs = [
        ("How do I know which IV therapy is right for me?", "Tell us how you are feeling and what you need to get back to. Your nurse reviews your health history at the appointment and will confirm or adjust the recommendation before anything starts."),
        ("Can I combine or customise treatments?", "Most drips can be adjusted with add-ons such as extra B12, magnesium, vitamin C or anti-nausea medication. Ask when you book and your nurse will confirm what is appropriate."),
        ("How long does each treatment take?", "Most therapies run 30 to 60 minutes. NAD+ is infused slowly on purpose and can take 90 minutes to three hours depending on dose."),
        ("How often can I have IV therapy?", "It depends entirely on the therapy and on you. Some people book monthly, others only when they are run down or travelling. Your nurse will give you a straight answer for your situation."),
        ("Are there side effects?", "The most common are a cool sensation in the arm, a metallic or vitamin taste, and mild bruising at the site. Serious reactions are rare, and your nurse stays with you throughout the treatment."),
        ("Do you take HSA or FSA cards?", "Yes, where your plan allows it. IV therapy is generally not covered by standard health insurance, so we keep pricing simple and all-in."),
    ]

    body = """
  <main id="main">
    <section class="page-hero">
      <div class="page-hero__media">%s</div>
      <div class="container">
        <div class="page-hero__inner">
          <ol class="breadcrumb"><li><a href="{{P}}index.html">Home</a></li><li>Services</li></ol>
          <span class="pill">17 IV therapies</span>
          <h1>IV Therapy Built Around <span style="color:var(--teal-300)">How You Feel</span></h1>
          <p>From hangovers and migraines to immunity, athletic recovery and skin health — every drip is delivered to you by a licensed registered nurse.</p>
          <a class="btn btn--lg" href="{{P}}contact.html#book">Book Your IV Therapy %s</a>
        </div>
      </div>
    </section>

    <section class="section" aria-labelledby="all-svc">
      <div class="container">
        <div class="section-head section-head--center reveal">
          <span class="eyebrow">Our full menu</span>
          <h2 id="all-svc">Choose Your <span class="text-accent">Therapy</span></h2>
          <p>Filter by what you need today. Every treatment includes the nurse visit, sterile supplies and a full assessment.</p>
        </div>

        %s
        <p class="center" style="color:var(--color-text-muted);font-size:var(--fs-sm);margin-bottom:2rem" data-filter-count aria-live="polite">Showing all %d therapies</p>

        %s

        <p class="center" data-filter-empty hidden style="color:var(--color-text-muted)">No therapies match that filter.</p>

        <p class="center measure" style="margin:3rem auto 0;color:var(--color-text-muted);font-size:var(--fs-sm)">
          Not sure which one to pick? Call us on <a href="tel:%s">%s</a> and we will talk it through — no pressure, and we will tell you if you do not need a drip at all.
        </p>
      </div>
    </section>

    <section class="section section--alt" aria-labelledby="svc-how">
      <div class="container">
        <div class="section-head section-head--center reveal">
          <span class="eyebrow">How it works</span>
          <h2 id="svc-how">Wellness Made <span class="text-accent">Simple</span></h2>
        </div>
        %s
      </div>
    </section>

    <section class="section" aria-labelledby="svc-inc">
      <div class="container">
        <div class="split">
          <div class="reveal">
            <span class="eyebrow">What is included</span>
            <h2 id="svc-inc">One Price. <span class="text-accent">Everything In It.</span></h2>
            <p class="lead">No call-out fees, no surprise add-ons at the door and no waiting-room time.</p>
            %s
          </div>
          <div class="about__media reveal" data-delay="2">
            %s
          </div>
        </div>
      </div>
    </section>

    <section class="section section--alt" aria-labelledby="svc-faq">
      <div class="container container--narrow">
        <div class="section-head section-head--center reveal">
          <span class="eyebrow">Questions</span>
          <h2 id="svc-faq">Service <span class="text-accent">FAQs</span></h2>
        </div>
        %s
      </div>
    </section>
  </main>
""" % (
        img("services-hero.jpg", "IV therapy bag and medical supplies prepared for a mobile appointment", 1600, 900, eager=True),
        icon("arrow-right", 18, "btn__icon"),
        filter_bar(), len(SERVICES),
        service_cards(),
        SITE["phone_href"], SITE["phone_display"],
        steps_html(),
        check_list([
            "A licensed registered nurse for the full appointment",
            "Full health assessment before any treatment begins",
            "Medical-grade fluids, vitamins and sterile supplies",
            "Treatment at your home, office, hotel or rental",
            "Aftercare guidance and safe disposal of all materials",
            "Honest advice — including when you do not need a drip",
        ], light=True),
        img("iv-drip-detail.jpg", "Close-up of a sterile IV drip line during a home treatment", 900, 675),
        faq_html(faqs),
    )

    page = (head_html(
        "IV Therapy Services in Orlando — All 17 Treatments | %s" % SITE["name"],
        "Explore all 17 mobile IV therapies from Orlando IV Care: hangover, migraine, immune boost, NAD+, glutathione, athletic recovery, beauty and more. Delivered to you.",
        SITE["domain"] + "/services",
        schema=faq_schema(faqs), og_image="services-hero.jpg")
        + header_html("services") + body + cta_band() + footer_html())
    write("services.html", page, 0)


def build_locations():
    cards = "".join("""
        <article class="loc-grid-card reveal" data-delay="%d">
          <div class="loc-grid-card__img">%s</div>
          <div class="loc-grid-card__body">
            <h3>%s</h3>
            <p>%s</p>
            <a class="link-arrow" href="{{P}}locations/%s.html">Explore %s %s</a>
          </div>
        </article>""" % ((i % 4) + 1,
                         img(l["img"], "Mobile IV therapy in %s" % l["name"], 800, 500),
                         l["name"], l["blurb"], l["slug"], l["name"], icon("arrow-right", 16))
        for i, l in enumerate(LOCATIONS))

    body = """
  <main id="main">
    <section class="page-hero">
      <div class="page-hero__media">%s</div>
      <div class="container">
        <div class="page-hero__inner">
          <ol class="breadcrumb"><li><a href="{{P}}index.html">Home</a></li><li>Locations</li></ol>
          <span class="pill">Serving Orlando &amp; surrounding areas</span>
          <h1>We Come to <span style="color:var(--teal-300)">You</span></h1>
          <p>Orlando IV Care serves homes, offices, hotels and vacation rentals across five communities — with the same nurses, the same protocols and the same all-in pricing everywhere.</p>
          <a class="btn btn--lg" href="{{P}}contact.html#book">Book Your IV Therapy %s</a>
        </div>
      </div>
    </section>

    <section class="section" aria-labelledby="loc-list">
      <div class="container">
        <div class="section-head section-head--center reveal">
          <span class="eyebrow">Where we serve</span>
          <h2 id="loc-list">Our <span class="text-accent">Locations</span></h2>
          <p>Choose your area to see local therapies, timings and answers to the questions we get asked most.</p>
        </div>
        <div class="grid grid-3">%s</div>

        <p class="center measure" style="margin:3rem auto 0;color:var(--color-text-muted);font-size:var(--fs-sm)">
          Not on the list? We often travel a little further for group bookings and events. Call <a href="tel:%s">%s</a> and we will tell you straight away whether we can reach you.
        </p>
      </div>
    </section>

    <section class="section section--alt" aria-labelledby="loc-how">
      <div class="container">
        <div class="section-head section-head--center reveal">
          <span class="eyebrow">How it works</span>
          <h2 id="loc-how">Same Service, <span class="text-accent">Wherever You Are</span></h2>
        </div>
        %s
      </div>
    </section>

    <section class="section why" aria-labelledby="loc-why">
      <div class="container">
        <div class="split">
          <div class="reveal">
            <span class="eyebrow">Mobile by design</span>
            <h2 id="loc-why">Care That Travels <span class="text-accent">Well</span></h2>
            <p>Everything your nurse needs arrives in one case: sterile fluids, medical-grade ingredients, monitoring equipment and a sharps container for safe disposal. Nothing is left behind.</p>
            %s
          </div>
          <div class="why__media reveal" data-delay="2">%s</div>
        </div>
      </div>
    </section>
  </main>
""" % (
        img("locations-hero.jpg", "Orlando skyline at dusk", 1600, 900, eager=True),
        icon("arrow-right", 18, "btn__icon"),
        cards,
        SITE["phone_href"], SITE["phone_display"],
        steps_html(),
        check_list([
            "Home, office, hotel, resort and rental visits",
            "Gated community and concierge-friendly arrivals",
            "Evening and weekend appointments available",
            "Group bookings at a single address",
            "No travel fee inside our core service area",
            "Discreet arrival — no branded vehicles or signage",
        ]),
        img("mobile-service.jpg", "Nurse arriving at a client's home with mobile IV therapy supplies", 900, 675),
    )

    page = (head_html(
        "Mobile IV Therapy Locations Across Orlando | %s" % SITE["name"],
        "Orlando IV Care delivers mobile IV therapy to Dr. Phillips, Lake Nona, Winter Park, Windermere and Celebration. Same nurses, same protocols, same pricing.",
        SITE["domain"] + "/locations",
        og_image="locations-hero.jpg")
        + header_html("locations") + body + cta_band() + footer_html())
    write("locations.html", page, 0)


def build_about():
    values = [
        ("shield-check", "Clinical first", "Every protocol is reviewed by a physician and every treatment is delivered by a licensed registered nurse. We assess before we treat, every time."),
        ("users", "Genuinely local", "We live and work in these communities. The nurse at your door is not passing through — they are your neighbour."),
        ("message-circle", "Straight answers", "If a drip will not help you, we will say so and point you somewhere that will. That has cost us bookings, and we are fine with it."),
        ("wallet", "Honest pricing", "One price, everything included. No call-out fee, no fuel surcharge, no upsell at the door when you are already in the chair."),
    ]
    value_cards = "".join("""
        <div class="value-card reveal" data-delay="%d">
          <span class="value-card__icon">%s</span>
          <h3>%s</h3>
          <p>%s</p>
        </div>""" % (i + 1, icon(ic, 28), t, d) for i, (ic, t, d) in enumerate(values))

    faqs = [
        ("Who administers the treatments?", "Licensed registered nurses with hospital or emergency experience, working under protocols approved by a supervising physician. Your nurse will introduce themselves and review your history before anything begins."),
        ("Is IV therapy safe?", "For most healthy adults, yes — it is a routine clinical procedure. Risks include bruising, irritation at the site and, rarely, an adverse reaction. Your nurse screens for contraindications and stays with you for the whole appointment."),
        ("Who should not have IV therapy?", "Anyone with certain kidney, heart or liver conditions, some medication interactions, or an allergy to an ingredient. Pregnant clients need clearance from their physician. We will decline treatment when it is not appropriate."),
        ("Do you treat children?", "No. We treat adults aged 18 and over only."),
        ("What areas do you cover?", "Dr. Phillips, Lake Nona, Winter Park, Windermere and Celebration, plus much of the surrounding Orlando area. Call us if you are unsure whether you are in range."),
    ]

    body = """
  <main id="main">
    <section class="page-hero">
      <div class="page-hero__media">%s</div>
      <div class="container">
        <div class="page-hero__inner">
          <ol class="breadcrumb"><li><a href="{{P}}index.html">Home</a></li><li>About Us</li></ol>
          <span class="pill">About %s</span>
          <h1>Clinical Care, <span style="color:var(--teal-300)">Without the Waiting Room</span></h1>
          <p>We are an Orlando team of registered nurses and clinicians who think good care should not cost you a day off work.</p>
          <a class="btn btn--lg" href="{{P}}contact.html#book">Book Your IV Therapy %s</a>
        </div>
      </div>
    </section>

    <section class="section" aria-labelledby="story">
      <div class="container">
        <div class="split">
          <div class="reveal">
            <span class="eyebrow">Our story</span>
            <h2 id="story">Built by People Who Were <span class="text-accent">Tired of the Wait</span></h2>
            <p class="lead">%s started with a simple observation: the treatment takes an hour, but getting it used to take a day.</p>
            <p>Our founders spent years in Orlando hospitals and urgent care watching otherwise healthy people give up an entire afternoon — parking, forms, waiting room, twenty minutes of care, waiting again — for hydration and vitamins that could have been delivered at their kitchen table.</p>
            <p>So we built the version we would want ourselves. Licensed registered nurses. Medical-grade ingredients from reputable pharmacies. Physician-approved protocols. And an appointment that comes to your door at a time that actually works for you.</p>
            <p>We are not a wellness fad with an IV pole. We are clinicians who made something genuinely useful more convenient.</p>
          </div>
          <div class="about__media reveal" data-delay="2">
            %s
            <span class="badge-float">%s Orlando owned &amp; operated</span>
          </div>
        </div>
      </div>
    </section>

    <section class="section section--alt" aria-labelledby="values">
      <div class="container">
        <div class="section-head section-head--center reveal">
          <span class="eyebrow">What we stand for</span>
          <h2 id="values">Our <span class="text-accent">Principles</span></h2>
        </div>
        <div class="grid grid-4">%s</div>
      </div>
    </section>

    <section class="section why" aria-labelledby="std">
      <div class="container">
        <div class="split split--reverse">
          <div class="reveal">
            <span class="eyebrow">Our standards</span>
            <h2 id="std">What We Will <span class="text-accent">Never Compromise On</span></h2>
            %s
            <a class="btn" href="{{P}}services.html">See our therapies %s</a>
          </div>
          <div class="why__media reveal" data-delay="2">%s</div>
        </div>
      </div>
    </section>

    <section class="section" aria-labelledby="numbers">
      <div class="container">
        <h2 id="numbers" class="visually-hidden">Orlando IV Care by the numbers</h2>
        <div class="stats">
          <div class="reveal"><div class="stat__num">5,000+</div><div class="stat__label">Treatments delivered</div></div>
          <div class="reveal" data-delay="1"><div class="stat__num">4.9&#9733;</div><div class="stat__label">Average client rating</div></div>
          <div class="reveal" data-delay="2"><div class="stat__num">17</div><div class="stat__label">IV therapies offered</div></div>
          <div class="reveal" data-delay="3"><div class="stat__num">5</div><div class="stat__label">Communities served</div></div>
        </div>
      </div>
    </section>

    <section class="section section--alt" aria-labelledby="about-faq">
      <div class="container container--narrow">
        <div class="section-head section-head--center reveal">
          <span class="eyebrow">Good to know</span>
          <h2 id="about-faq">Common <span class="text-accent">Questions</span></h2>
        </div>
        %s
      </div>
    </section>
  </main>
""" % (
        img("about-hero.jpg", "Registered nurse smiling while preparing an IV treatment", 1600, 900, eager=True),
        SITE["name"], icon("arrow-right", 18, "btn__icon"),
        SITE["name"],
        img("about-nurse.jpg", "Orlando IV Care registered nurse with treatment supplies", 900, 675),
        icon("map-pin", 20),
        value_cards,
        check_list([
            "Registered nurses only — never unlicensed staff",
            "Physician-approved treatment protocols",
            "Ingredients from reputable, regulated pharmacies",
            "Full health screening before every treatment",
            "Single-use sterile supplies, safely disposed of",
            "The right to decline treatment when it is not safe",
        ]),
        icon("arrow-right", 18, "btn__icon"),
        img("standards.jpg", "Sterile single-use IV supplies laid out before a treatment", 900, 675),
        faq_html(faqs),
    )

    page = (head_html(
        "About Orlando IV Care — Licensed Nurses, Mobile IV Therapy",
        "Orlando IV Care is a locally owned mobile IV therapy service run by registered nurses under physician-approved protocols. Meet the team and our standards.",
        SITE["domain"] + "/about",
        schema=faq_schema(faqs), og_image="about-hero.jpg")
        + header_html("about") + body + cta_band() + footer_html())
    write("about.html", page, 0)


def build_contact():
    loc_options = "".join('<option value="%s">%s</option>' % (l["name"], l["name"]) for l in LOCATIONS)
    svc_options = "".join('<option value="%s">%s</option>' % (s["name"], s["name"]) for s in SERVICES)

    body = """
  <main id="main">
    <section class="page-hero">
      <div class="page-hero__media">%s</div>
      <div class="container">
        <div class="page-hero__inner">
          <ol class="breadcrumb"><li><a href="{{P}}index.html">Home</a></li><li>Contact</li></ol>
          <span class="pill">Same-day appointments</span>
          <h1>Book Your <span style="color:var(--teal-300)">IV Therapy</span></h1>
          <p>Tell us where you are, what you need and when suits you. We will confirm your appointment — usually within the hour during opening times.</p>
        </div>
      </div>
    </section>

    <section class="section" id="book" aria-labelledby="book-h">
      <div class="container">
        <div class="split" style="align-items:start">

          <div class="reveal">
            <span class="eyebrow">Booking request</span>
            <h2 id="book-h">Request an <span class="text-accent">Appointment</span></h2>
            <p class="lead">Prefer to talk it through? Call <a href="tel:%s">%s</a> — we would rather answer your questions than have you guess.</p>

            <div class="stack mt-6">
              <div class="info-tile">
                <span class="info-tile__icon">%s</span>
                <div><h3>Call or text</h3><a href="tel:%s">%s</a></div>
              </div>
              <div class="info-tile">
                <span class="info-tile__icon">%s</span>
                <div><h3>Email</h3><a href="mailto:%s">%s</a></div>
              </div>
              <div class="info-tile">
                <span class="info-tile__icon">%s</span>
                <div><h3>Opening hours</h3><p>%s</p></div>
              </div>
              <div class="info-tile">
                <span class="info-tile__icon">%s</span>
                <div><h3>Service area</h3><p>Dr. Phillips, Lake Nona, Winter Park, Windermere, Celebration and surrounding Orlando communities.</p></div>
              </div>
            </div>
          </div>

          <div class="form-card reveal" data-delay="2">
            <form data-validate-form novalidate>
              <div class="form-summary" role="alert"></div>

              <div class="form-grid">
                <div class="field">
                  <label for="f-name">Full name <span class="req" aria-hidden="true">*</span></label>
                  <input id="f-name" name="name" type="text" autocomplete="name" data-validate="name" required aria-describedby="e-name">
                  <span class="field__error" id="e-name" role="alert"></span>
                </div>

                <div class="field">
                  <label for="f-phone">Phone <span class="req" aria-hidden="true">*</span></label>
                  <input id="f-phone" name="phone" type="tel" inputmode="tel" autocomplete="tel" data-validate="tel" required aria-describedby="e-phone">
                  <span class="field__error" id="e-phone" role="alert"></span>
                </div>

                <div class="field field--full">
                  <label for="f-email">Email <span class="req" aria-hidden="true">*</span></label>
                  <input id="f-email" name="email" type="email" inputmode="email" autocomplete="email" data-validate="email" required aria-describedby="e-email">
                  <span class="field__error" id="e-email" role="alert"></span>
                </div>

                <div class="field">
                  <label for="f-location">Your area <span class="req" aria-hidden="true">*</span></label>
                  <select id="f-location" name="location" required aria-describedby="e-location">
                    <option value="">Select an area…</option>
                    %s
                    <option value="Other">Somewhere else in Orlando</option>
                  </select>
                  <span class="field__error" id="e-location" role="alert"></span>
                </div>

                <div class="field">
                  <label for="f-service">Therapy <span class="req" aria-hidden="true">*</span></label>
                  <select id="f-service" name="service" required aria-describedby="e-service">
                    <option value="">Select a therapy…</option>
                    %s
                    <option value="Not sure">Not sure — please advise</option>
                  </select>
                  <span class="field__error" id="e-service" role="alert"></span>
                </div>

                <div class="field">
                  <label for="f-date">Preferred date</label>
                  <input id="f-date" name="date" type="date">
                  <span class="field__help" id="h-date">Leave blank for the earliest available slot.</span>
                </div>

                <div class="field">
                  <label for="f-time">Preferred time</label>
                  <select id="f-time" name="time">
                    <option value="">No preference</option>
                    <option value="Morning">Morning (8am – 12pm)</option>
                    <option value="Afternoon">Afternoon (12pm – 5pm)</option>
                    <option value="Evening">Evening (5pm – 9pm)</option>
                  </select>
                </div>

                <div class="field field--full">
                  <label for="f-notes">Anything we should know?</label>
                  <textarea id="f-notes" name="notes" rows="4" aria-describedby="h-notes"></textarea>
                  <span class="field__help" id="h-notes">Gate codes, group size, allergies, medications, or how you are feeling today.</span>
                </div>
              </div>

              <button class="btn btn--lg btn--block mt-5" type="submit">
                %s
                <span>Request my appointment</span>
                %s
              </button>

              <p class="form-note">
                By sending this request you agree to be contacted about your appointment. This form is a request,
                not a confirmation — we will contact you to confirm. For a medical emergency, call 911.
              </p>

              <div class="form-status" role="status" aria-live="polite">
                %s
                <span><strong>Request received.</strong> Thank you — we will contact you shortly to confirm your appointment time. If you need us urgently, call <a href="tel:%s">%s</a>.</span>
              </div>
            </form>
          </div>

        </div>
      </div>
    </section>

    <section class="section section--alt" aria-labelledby="c-how">
      <div class="container">
        <div class="section-head section-head--center reveal">
          <span class="eyebrow">What happens next</span>
          <h2 id="c-how">From Request to <span class="text-accent">Relief</span></h2>
        </div>
        %s
      </div>
    </section>
  </main>
""" % (
        img("contact-hero.jpg", "Comfortable home setting prepared for a mobile IV therapy appointment", 1600, 900, eager=True),
        SITE["phone_href"], SITE["phone_display"],
        icon("phone", 22), SITE["phone_href"], SITE["phone_display"],
        icon("mail", 22), SITE["email"], SITE["email"],
        icon("clock", 22), SITE["hours"],
        icon("map-pin", 22),
        loc_options, svc_options,
        icon("loader", 18, "btn__spinner"),
        icon("arrow-right", 18, "btn__icon"),
        icon("check-circle", 22),
        SITE["phone_href"], SITE["phone_display"],
        steps_html(),
    )

    page = (head_html(
        "Book Mobile IV Therapy in Orlando | Contact %s" % SITE["name"],
        "Request a same-day mobile IV therapy appointment anywhere in Orlando. Call, email or send a booking request and a licensed nurse will come to you.",
        SITE["domain"] + "/contact", og_image="contact-hero.jpg")
        + header_html("contact") + body + cta_band() + footer_html())
    write("contact.html", page, 0)


def build_location(loc):
    why_cards = "".join("""
        <div class="value-card reveal" data-delay="%d">
          <span class="value-card__icon">%s</span>
          <h3>%s</h3>
          <p>%s</p>
        </div>""" % (i + 1, icon(["map-pin", "clock", "shield-check", "users"][i % 4], 28), t, d)
        for i, (t, d) in enumerate(loc["why"]))

    body = """
  <main id="main">
    <section class="page-hero">
      <div class="page-hero__media">%s</div>
      <div class="container">
        <div class="page-hero__inner">
          <ol class="breadcrumb">
            <li><a href="{{P}}index.html">Home</a></li>
            <li><a href="{{P}}locations.html">Locations</a></li>
            <li>%s</li>
          </ol>
          <span class="pill">Mobile IV therapy &middot; %s</span>
          <h1>IV Therapy in <span style="color:var(--teal-300)">%s</span></h1>
          <p>%s</p>
          <a class="btn btn--lg" href="{{P}}contact.html#book">Book Your IV Therapy %s</a>
        </div>
      </div>
    </section>

    <section class="section" aria-labelledby="l-intro">
      <div class="container">
        <div class="split">
          <div class="reveal">
            <span class="eyebrow">Serving %s</span>
            <h2 id="l-intro">Care That Comes to <span class="text-accent">Your Door</span></h2>
            <p class="lead">%s</p>
            <p>Every appointment is delivered by a licensed registered nurse working under physician-approved protocols, using medical-grade ingredients. You get a full assessment before anything starts, and honest advice about whether a drip is right for you today.</p>
            <a class="link-arrow mt-5" href="{{P}}services.html">See all 17 therapies %s</a>
          </div>
          <div class="about__media reveal" data-delay="2">
            %s
            <span class="badge-float">%s Serving %s &amp; nearby</span>
          </div>
        </div>
      </div>
    </section>

    <section class="section section--alt" aria-labelledby="l-why">
      <div class="container">
        <div class="section-head section-head--center reveal">
          <span class="eyebrow">Why %s books with us</span>
          <h2 id="l-why">Local Needs, <span class="text-accent">Local Care</span></h2>
        </div>
        <div class="grid grid-4">%s</div>
      </div>
    </section>

    <section class="section" aria-labelledby="l-svc">
      <div class="container">
        <div class="section-head section-head--center reveal">
          <span class="eyebrow">Popular in %s</span>
          <h2 id="l-svc">Most-Booked <span class="text-accent">Therapies</span></h2>
          <p>These are the drips %s residents and visitors ask for most — but all 17 are available here.</p>
        </div>
        <div class="reveal">%s</div>
        <div class="center mt-6"><a class="btn btn--ghost" href="{{P}}services.html">View All Services %s</a></div>
      </div>
    </section>

    <section class="section section--alt" aria-labelledby="l-how">
      <div class="container">
        <div class="section-head section-head--center reveal">
          <span class="eyebrow">How it works in %s</span>
          <h2 id="l-how">Booked, Treated, <span class="text-accent">Back to Normal</span></h2>
        </div>
        %s
      </div>
    </section>

    <section class="section why" aria-labelledby="l-ben">
      <div class="container">
        <div class="split split--reverse">
          <div class="reveal">
            <span class="eyebrow">The benefits</span>
            <h2 id="l-ben">Why At-Home Beats <span class="text-accent">The Waiting Room</span></h2>
            <p>An hour of your day, in your own chair, with someone qualified doing the work — instead of half a day spent getting to and from a clinic.</p>
            %s
            <a class="btn" href="{{P}}contact.html#book">Book in %s %s</a>
          </div>
          <div class="why__media reveal" data-delay="2">%s</div>
        </div>
      </div>
    </section>

    <section class="section" aria-labelledby="l-testi">
      <div class="container">
        <div class="section-head section-head--center reveal">
          <span class="eyebrow">%s clients</span>
          <h2 id="l-testi">What People Here <span class="text-accent">Say</span></h2>
        </div>
        %s
      </div>
    </section>

    <section class="section section--alt" aria-labelledby="l-faq">
      <div class="container container--narrow">
        <div class="section-head section-head--center reveal">
          <span class="eyebrow">%s questions</span>
          <h2 id="l-faq">Frequently <span class="text-accent">Asked</span></h2>
        </div>
        %s
      </div>
    </section>

    <section class="section section--dark" aria-labelledby="l-cta">
      <div class="container container--narrow cta-center">
        <div class="reveal">
          <span class="eyebrow">%s</span>
          <h2 id="l-cta">Feel Better <span class="text-accent">Today</span></h2>
          <p class="lead">Same-day appointments are usually available in %s. Tell us when suits you.</p>
          <div class="btn-row">
            <a class="btn btn--lg" href="{{P}}contact.html#book">Book Now %s</a>
            <a class="btn btn--outline-light btn--lg" href="tel:%s">%s %s</a>
          </div>
        </div>
      </div>
    </section>
  </main>
""" % (
        img(loc["img"], "Mobile IV therapy serving %s, Orlando" % loc["name"], 1600, 900, eager=True),
        loc["name"], loc["name"], loc["name"], loc["blurb"], icon("arrow-right", 18, "btn__icon"),
        loc["name"], loc["intro"], icon("arrow-right", 16),
        img("mobile-service.jpg", "Nurse arriving for a mobile IV therapy appointment", 900, 675),
        icon("map-pin", 20), loc["name"],
        loc["name"], why_cards,
        loc["name"], loc["name"], service_mini_grid(names=loc["popular"]), icon("arrow-right", 18, "btn__icon"),
        loc["name"], steps_html(),
        check_list([
            "No driving, parking or waiting room time",
            "Treatment in your own home, hotel or rental",
            "Licensed registered nurse for the full hour",
            "Same-day and evening appointments",
            "Group bookings at one address",
            "One all-in price with no travel fee",
        ]),
        loc["name"], icon("arrow-right", 18, "btn__icon"),
        img("why-choose-iv-care.jpg", "IV therapy supplies prepared for a home visit", 900, 675),
        loc["name"], testimonials_html(loc["testimonials"]),
        loc["name"], faq_html(loc["faqs"]),
        loc["name"], loc["name"],
        icon("arrow-right", 18, "btn__icon"),
        SITE["phone_href"], icon("phone", 18), SITE["phone_display"],
    )

    schema = faq_schema(loc["faqs"])
    page = (head_html(
        "Mobile IV Therapy in %s, Orlando | %s" % (loc["name"], SITE["name"]),
        "%s Licensed nurses, medical-grade ingredients and same-day appointments in %s." % (loc["blurb"], loc["name"]),
        "%s/locations/%s" % (SITE["domain"], loc["slug"]),
        schema=schema, og_image=loc["img"])
        + header_html("locations") + body + cta_band() + footer_html())
    write("locations/%s.html" % loc["slug"], page, 1)


def build_sitemap():
    urls = ["/", "/services", "/locations", "/about", "/contact"] + ["/locations/%s" % l["slug"] for l in LOCATIONS]
    items = "".join('\n  <url><loc>%s%s</loc><changefreq>monthly</changefreq><priority>%s</priority></url>'
                    % (SITE["domain"], u, "1.0" if u == "/" else "0.8") for u in urls)
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">%s\n</urlset>\n' % items
    write("sitemap.xml", xml, 0)

    robots = "User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n" % SITE["domain"]
    write("robots.txt", robots, 0)


def main():
    print("Building %s…" % SITE["name"])
    build_home()
    build_services()
    build_locations()
    build_about()
    build_contact()
    for loc in LOCATIONS:
        build_location(loc)
    build_sitemap()
    print("Done. %d pages." % (5 + len(LOCATIONS)))


if __name__ == "__main__":
    main()
