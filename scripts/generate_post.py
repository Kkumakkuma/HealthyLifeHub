"""
HealthyLifeHub Auto Post Generator
Generates SEO-optimized health & wellness articles using OpenAI GPT API
"""

from openai import OpenAI
import datetime
import os
import random
import re

# High CPC keyword categories for health & wellness
TOPIC_POOLS = {
    "weight_loss": [
        "How to Lose Weight Without Starving Yourself",
        "{number} Proven Ways to Lose Belly Fat in {year}",
        "Intermittent Fasting for Beginners: Complete Guide",
        "How to Lose 10 Pounds in a Month Safely",
        "Why Most Diets Fail and What Actually Works",
        "Best Foods for Weight Loss You Should Eat Daily",
        "How to Speed Up Your Metabolism Naturally",
    ],
    "nutrition": [
        "{number} Superfoods You Should Eat Every Day",
        "Mediterranean Diet: Complete Beginner's Guide {year}",
        "How to Read Nutrition Labels Like a Pro",
        "Best Vitamins and Supplements for {year}",
        "Anti-Inflammatory Foods That Fight Disease",
        "How Much Protein Do You Really Need Per Day",
        "Gut Health: {number} Foods That Improve Digestion",
    ],
    "fitness": [
        "Best Home Workouts That Need No Equipment",
        "{number}-Minute Morning Workout to Start Your Day",
        "How to Build Muscle at Home Without Weights",
        "Walking for Weight Loss: How Many Steps Per Day",
        "Yoga for Beginners: {number} Poses You Should Know",
        "How to Start Running When You Are Out of Shape",
        "Best Exercises for Lower Back Pain Relief",
    ],
    "mental_health": [
        "How to Reduce Stress and Anxiety Naturally",
        "{number} Science-Backed Ways to Improve Your Mood",
        "Meditation for Beginners: How to Start Today",
        "How to Sleep Better: {number} Tips That Actually Work",
        "Signs of Burnout and How to Recover",
        "How Exercise Improves Your Mental Health",
        "Digital Detox: How to Reduce Screen Time for Better Health",
    ],
    "sleep": [
        "How to Fall Asleep in {number} Minutes or Less",
        "Best Sleep Supplements That Actually Work in {year}",
        "Why You Wake Up Tired and How to Fix It",
        "The Perfect Bedtime Routine for Better Sleep",
        "How Sleep Affects Weight Loss and Muscle Growth",
        "Best Sleeping Positions for Back Pain Relief",
        "{number} Habits That Are Ruining Your Sleep Quality",
    ],
    "skin_care": [
        "Best Skincare Routine for Beginners in {year}",
        "How to Get Rid of Acne Naturally",
        "{number} Anti-Aging Tips That Actually Work",
        "Best Sunscreens for Every Skin Type in {year}",
        "How to Build a Simple Skincare Routine on a Budget",
        "Foods That Improve Your Skin Health",
        "How to Reduce Dark Circles Under Your Eyes",
    ],
    "supplements": [
        "Best Multivitamins for Men and Women in {year}",
        "Vitamin D: How Much Do You Really Need",
        "Omega-3 Fish Oil Benefits and Side Effects",
        "Probiotics Guide: Best Supplements for Gut Health",
        "Magnesium Benefits: Why Most People Are Deficient",
        "Collagen Supplements: Do They Actually Work",
        "Best Pre-Workout Supplements Reviewed {year}",
    ],
    "disease_prevention": [
        "How to Lower Blood Pressure Naturally",
        "{number} Ways to Reduce Your Risk of Heart Disease",
        "Early Signs of Diabetes You Should Not Ignore",
        "How to Boost Your Immune System Naturally",
        "Foods That Lower Cholesterol Levels",
        "How to Prevent Common Nutrient Deficiencies",
        "{number} Cancer Prevention Tips Backed by Science",
    ],
}

SYSTEM_PROMPT = """You are an expert health and wellness writer for a blog called HealthyLifeHub.
Write SEO-optimized, informative, and engaging blog posts.

Rules:
- Write in a friendly, conversational but authoritative tone
- Use short paragraphs (2-3 sentences max)
- Include practical, actionable advice
- Use headers (##) to break up sections
- Include bullet points and numbered lists where appropriate
- Write between 1200-1800 words
- Naturally include the main keyword 3-5 times
- Include a compelling introduction that hooks the reader
- End with a clear conclusion/call-to-action
- Do NOT include any AI disclaimers or mentions of being AI-generated
- Write as if you are a certified health professional sharing expertise
- Always include a disclaimer like "consult your doctor before making changes"
- Make content evergreen where possible
- Include specific numbers and examples
- Do NOT use markdown title (# Title) - just start with the content
"""


def pick_topic():
    """Select a random topic from the pools."""
    year = datetime.datetime.now().year
    number = random.choice([3, 5, 7, 10, 12, 15])
    category = random.choice(list(TOPIC_POOLS.keys()))
    title_template = random.choice(TOPIC_POOLS[category])
    title = title_template.format(year=year, number=number)
    return title, category


def generate_post_content(title, category):
    """Generate a blog post using OpenAI GPT API."""
    client = OpenAI()

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        max_tokens=4000,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"Write a comprehensive blog post with the title: \"{title}\"\n\nCategory: {category.replace('_', ' ')}\n\nRemember to write 1200-1800 words, use ## for section headers, and make it SEO-friendly.",
            },
        ],
    )

    return response.choices[0].message.content


def slugify(title):
    """Convert title to URL-friendly slug."""
    slug = title.lower()
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)
    slug = re.sub(r'[\s]+', '-', slug)
    slug = re.sub(r'-+', '-', slug)
    slug = slug.strip('-')
    return slug


def get_repo_root():
    """Get the repository root directory."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.dirname(script_dir)


def get_existing_titles():
    """Get titles of existing posts to avoid duplicates."""
    posts_dir = os.path.join(get_repo_root(), '_posts')
    titles = set()
    if os.path.exists(posts_dir):
        for filename in os.listdir(posts_dir):
            if filename.endswith('.md'):
                title_part = filename[11:-3]
                titles.add(title_part)
    return titles


def create_post():
    """Generate and save a new blog post."""
    existing = get_existing_titles()

    for _ in range(10):
        title, category = pick_topic()
        slug = slugify(title)
        if slug not in existing:
            break
    else:
        title, category = pick_topic()
        slug = slugify(title) + f"-{random.randint(100, 999)}"

    print(f"Generating post: {title}")
    print(f"Category: {category}")

    content = generate_post_content(title, category)

    today = datetime.datetime.now()
    date_str = today.strftime('%Y-%m-%d')
    filename = f"{date_str}-{slug}.md"

    posts_dir = os.path.join(get_repo_root(), '_posts')
    os.makedirs(posts_dir, exist_ok=True)

    filepath = os.path.join(posts_dir, filename)

    frontmatter = f"""---
layout: post
title: "{title}"
date: {today.strftime('%Y-%m-%d %H:%M:%S')} +0000
categories: [{category.replace('_', '-')}]
description: "{title} - Evidence-based health and wellness tips for a healthier life."
---

{content}
"""

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(frontmatter)

    print(f"Post saved: {filepath}")
    return filepath, filename


if __name__ == '__main__':
    filepath, filename = create_post()
    print(f"Done! Post generated: {filename}")
