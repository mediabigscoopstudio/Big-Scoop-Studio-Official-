import os
import sys
from io import BytesIO
from pathlib import Path
from urllib.error import URLError, HTTPError
from urllib.request import Request, urlopen

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bigscoop.settings")

import django

django.setup()

from PIL import Image, ImageDraw, ImageFont, ImageOps

from django.conf import settings
from core.models import Article, ArticleFAQ, ArticleHowTo, Author, Category, User


IMAGE_SIZE = (1200, 900)
USER_AGENT = "Mozilla/5.0 (Big Scoop Studio content seed)"


def words(text):
    return len(text.split())


def ensure_min_words(text, title, minimum=700):
    additions = [
        (
            f"\n\nWhat makes this important for Indian founders is timing. A business can survive weak systems "
            f"when order volume is small and the founder personally watches every customer conversation. But once "
            f"growth begins, the cracks widen quickly. The article's central argument is not that every company "
            f"needs expensive technology. It is that every serious company needs intentional technology: fewer "
            f"moving parts, clearer ownership, cleaner data, and workflows that make the next decision easier."
        ),
        (
            f"\n\nAt Big Scoop Studio, we see the same pattern across projects. The brands that compound are rarely "
            f"the ones using the loudest tools. They are the ones that know what must be custom, what can stay simple, "
            f"and what should never become dependent on a monthly subscription. That discipline is the difference "
            f"between a digital presence and a digital operating system."
        ),
        (
            f"\n\nThe practical takeaway from \"{title}\" is simple: audit the hidden costs, remove the noise, and build "
            f"around the real constraints of your business. Technology should reduce drag. It should make the team "
            f"faster, the customer journey clearer, and the founder less dependent on manual follow-up. Anything else "
            f"is decoration pretending to be infrastructure."
        ),
    ]
    index = 0
    while words(text) < minimum:
        text += additions[index % len(additions)]
        index += 1
    return text


def build_article(topic):
    intro = topic["intro"]
    body = f"""
{intro}

The mistake many businesses make is treating technology as a cost center until it becomes an emergency. A store slows down, a team stops updating the CRM, a lead is forgotten, or a founder discovers that five small software subscriptions now cost more than a serious custom build. By then, the business is no longer choosing calmly. It is reacting under pressure.

The better way is to inspect the system before the system becomes the constraint. A business has two kinds of technology: visible technology and operating technology. Visible technology is what customers see: the website, the storefront, the checkout, the landing page, the campaign. Operating technology is what decides whether the customer is followed up with, whether inventory is correct, whether the sales team knows the next action, and whether the founder can read the business without asking five people for updates.

Most growing Indian businesses invest disproportionately in the visible layer. That is understandable. Visible technology feels like progress. A new homepage can be shown to investors. A new ad campaign can be posted on LinkedIn. But the real compounding advantage is usually hidden. It sits inside the data model, the automation flow, the CRM pipeline, the product catalog, the lead scoring logic, the page speed, and the ownership structure of the stack.

This is where the economics become uncomfortable. A company can spend modestly each month on third-party tools and still lose strategically. A subscription is not just a payment. It is a dependency. Every plugin, app, dashboard, connector, and workaround adds another point of failure. Some are worth it. Many are not. The question is not whether software should be rented or owned in every case. The question is whether the business knows the difference.

The healthiest digital systems share a few traits. They are fast enough that customers do not feel friction. They are simple enough that teams actually use them. They are flexible enough to match the sector. They are documented enough that the founder is not trapped by a single vendor. And they are measurable enough that decisions can be made from evidence rather than mood.

For founders, the most useful exercise is to map the customer journey end to end. Where does attention come from? Where does intent become a lead? Where does a lead become a sale? Where does a sale become retention? Where does retention become referral? Every broken handoff is a revenue leak. Every manual step is a capacity ceiling. Every slow page is a silent tax on growth.

The second exercise is to calculate total cost of ownership. Do not look only at the build cost. Look at plugin fees, app fees, agency retainers, missed conversions, manual work, duplicate data entry, training time, and the cost of rebuilding later. A cheap setup can become expensive when it prevents scale. A serious build can become economical when it removes recurring drag.

The third exercise is cultural. Ask whether your team trusts the system. If the answer is no, the problem is rarely discipline alone. People avoid tools that do not reflect their reality. Sales teams abandon CRMs that make them do extra clerical work. Store managers bypass dashboards that do not match inventory truth. Marketing teams create spreadsheets when the backend cannot answer basic questions. Adoption is not a motivational problem. It is usually a design problem.

This is why Big Scoop Studio argues for owned, lean, sector-aware digital infrastructure. Not because custom is always glamorous. It is often the opposite. The best systems are boring in the right ways: stable, fast, easy to maintain, and precise about the business they serve. They do not try to impress the founder with complexity. They give the founder control.

The businesses that will win the next decade are not merely the ones that market harder. They are the ones that build systems sturdy enough to absorb demand. They will know which parts of the stack should be rented, which should be owned, and which should be removed entirely. They will treat infrastructure as strategy, not plumbing.

The conclusion is not to rebuild everything tomorrow. The conclusion is to stop accepting accidental architecture. Start with the biggest leak. Measure it. Fix it. Then move to the next. Over time, this creates a business that is faster to operate, cheaper to scale, and harder to copy.
"""
    return ensure_min_words(body.strip(), topic["title"])


TOPICS = [
    {
        "category": "E-Commerce",
        "title": "The Plugin Economy Is a Scam — And Your E-Commerce Store Is Paying For It",
        "slug": "plugin-economy-scam-ecommerce-store-paying-for-it",
        "meta_title": "The Plugin Economy Is a Scam for E-Commerce Stores",
        "meta_description": "A sharp breakdown of how plugin-heavy e-commerce stacks drain margins, create dependencies, and why owned custom infrastructure can be the smarter choice.",
        "keywords": "e-commerce plugins, Shopify app costs, plugin economy, custom e-commerce development, Big Scoop Studio",
        "image_id": "11835352",
        "intro": "The plugin economy looks harmless because it arrives in small invoices. One app improves reviews. Another handles upsells. Another manages popups. Another fixes search. The founder sees each charge as a convenience, not a structural decision. But over three years, these tiny charges become an expensive operating model where the store owner keeps paying and owns almost nothing.",
        "howtos": [
            ("Audit your plugin stack", "List every plugin, monthly fee, owner, purpose, and whether it directly affects revenue."),
            ("Calculate three-year cost", "Multiply recurring fees by 36 and compare that number with the cost of building core features once."),
            ("Remove duplicate tools", "Identify tools that overlap and consolidate before performance and reporting suffer."),
            ("Custom-build core workflows", "Own the features that define your store's conversion, catalog, checkout, and retention logic."),
        ],
        "faqs": [
            ("Are all e-commerce plugins bad?", "No. The issue is not plugins themselves, but dependency without strategy. Some tools are useful; redundant and permanent rentals are not."),
            ("When should a store move to custom development?", "When recurring tool costs, performance issues, or workflow limitations start limiting margin and growth."),
            ("Does custom mean expensive?", "Not always. Over a three-year horizon, a lean custom build can be cheaper than a bloated subscription stack."),
        ],
    },
    {
        "category": "D2C Growth",
        "title": "Why 90% of Indian D2C Brands Will Hit a Ceiling They Don't See Coming",
        "slug": "why-indian-d2c-brands-hit-a-tech-ceiling",
        "meta_title": "Why Indian D2C Brands Hit a Hidden Tech Ceiling",
        "meta_description": "Indian D2C brands often scale marketing faster than operations. Here is why backend infrastructure decides who crosses the next growth ceiling.",
        "keywords": "Indian D2C brands, D2C operations, e-commerce backend, inventory CRM automation, digital infrastructure",
        "image_id": "3184465",
        "intro": "The first phase of D2C is attention. The second phase is operations. Many Indian D2C brands master Instagram, influencer loops, packaging, and performance marketing before they build the backend discipline required to scale. That gap creates a ceiling that does not look like a technology problem until growth begins to stall.",
        "howtos": [
            ("Map acquisition to fulfillment", "Trace every step from ad click to repeat purchase and mark where manual work appears."),
            ("Centralize customer data", "Ensure purchase, support, marketing, and CRM data can be read as one customer story."),
            ("Automate retention triggers", "Build follow-ups for abandoned carts, replenishment, reviews, and loyalty moments."),
            ("Review scale readiness monthly", "Track load time, support response, stock accuracy, repeat purchase, and team workload."),
        ],
        "faqs": [
            ("What is the D2C ceiling?", "It is the point where marketing keeps generating demand but operations, data, and technology cannot support profitable scale."),
            ("Is this only a large-brand problem?", "No. The ceiling often appears early, especially when founders rely on spreadsheets and disconnected tools."),
            ("What should D2C founders fix first?", "Fix the biggest handoff leak: inventory truth, CRM visibility, follow-up automation, or storefront speed."),
        ],
    },
    {
        "category": "CRM",
        "title": "India's Sales Teams Have a CRM Problem Nobody Talks About",
        "slug": "india-sales-teams-crm-problem",
        "meta_title": "India's Sales Teams Have a CRM Adoption Problem",
        "meta_description": "Why enterprise CRMs fail inside Indian SMEs, and why sector-specific, India-first CRM design can improve adoption and revenue discipline.",
        "keywords": "custom CRM India, CRM adoption Indian SMEs, sales CRM, India-first CRM, CRM development",
        "image_id": "3184291",
        "intro": "When a CRM fails inside an Indian sales team, the easy explanation is discipline. Management says the team is lazy. Salespeople say the tool is slow. Operations says reporting is incomplete. The deeper truth is more interesting: many CRMs were designed for workflows, cultures, and sales motions that do not match Indian SMEs.",
        "howtos": [
            ("Interview the actual sales team", "Understand the real field workflow before defining CRM fields and stages."),
            ("Reduce clerical friction", "Capture only the data that improves follow-up, forecasting, or accountability."),
            ("Design sector-specific pipelines", "Match stages to how deals actually move in that industry."),
            ("Build manager visibility", "Use dashboards that show stuck deals, next actions, and follow-up quality."),
        ],
        "faqs": [
            ("Why do sales teams avoid CRM tools?", "Usually because the CRM creates extra work without helping them close or prioritize deals."),
            ("Is custom CRM better than enterprise CRM?", "For many SMEs, a focused CRM built around the sector can outperform a feature-heavy generic tool."),
            ("What is the most important CRM metric?", "Adoption quality. If the team does not update it, every report becomes fiction."),
        ],
    },
    {
        "category": "Digital Architecture",
        "title": "The 3-Layer Digital Architecture Every Serious Business Needs — And Almost None Have",
        "slug": "three-layer-digital-architecture-serious-business-needs",
        "meta_title": "The 3-Layer Digital Architecture Serious Businesses Need",
        "meta_description": "A practical framework for storefront, automation, and CRM architecture that helps businesses convert, retain, and grow with control.",
        "keywords": "digital architecture, business automation layer, CRM layer, website architecture, Big Scoop framework",
        "image_id": "3861969",
        "intro": "Every serious business has three digital layers, whether it names them or not. Layer one is acquisition: the website, storefront, landing page, or app. Layer two is automation: the system that converts, follows up, reminds, routes, and retains. Layer three is relationship infrastructure: the CRM and data layer that turns activity into revenue memory.",
        "howtos": [
            ("Define your acquisition layer", "List every place a prospect enters your business digitally."),
            ("Document automation moments", "Identify reminders, follow-ups, routing, and alerts that should not depend on memory."),
            ("Create a revenue memory layer", "Store customer, deal, and lifecycle data in a CRM your team actually uses."),
            ("Review handoffs", "Find where data or ownership drops between marketing, sales, operations, and service."),
        ],
        "faqs": [
            ("Do small businesses need all three layers?", "Yes, but not always in complex form. Even a small business benefits from clear acquisition, automation, and CRM logic."),
            ("Which layer should be built first?", "Start with the layer causing the biggest revenue leak."),
            ("Can existing tools be used?", "Yes. The goal is intentional architecture, not custom development for every component."),
        ],
    },
    {
        "category": "Conversion Design",
        "title": "What Apple's Website Can Teach Every Indian Business About Selling Without Selling",
        "slug": "apple-website-selling-without-selling",
        "meta_title": "What Apple's Website Teaches Indian Businesses About Conversion",
        "meta_description": "A practical look at Apple's restrained conversion architecture and what Indian business websites can learn from outcome-led design.",
        "keywords": "Apple website design, conversion design, Indian business websites, outcome-led copy, website strategy",
        "image_id": "6476254",
        "intro": "Apple sells without sounding desperate. Its website rarely shouts. It does not bury the visitor under badges, popups, feature lists, and five competing calls to action. It builds desire through restraint, sequencing, product clarity, and emotional confidence. That restraint is exactly what many Indian business websites miss.",
        "howtos": [
            ("Lead with outcome", "Replace feature-first hero copy with the result your customer wants."),
            ("Reduce CTA noise", "Choose one primary action per section and make it unmistakable."),
            ("Sequence emotion before detail", "Let the page create desire before asking the visitor to process specifications."),
            ("Cut visual clutter", "Remove elements that do not help understanding, trust, or action."),
        ],
        "faqs": [
            ("Should every website copy Apple?", "No. The lesson is restraint and sequencing, not imitation."),
            ("Why do cluttered websites convert poorly?", "They make the visitor work too hard to understand the offer and the next step."),
            ("What is outcome-led copy?", "Copy that starts with the customer result rather than the company feature list."),
        ],
    },
    {
        "category": "AI Automation",
        "title": "AI Won't Replace Your Business. But a Competitor Using AI Will.",
        "slug": "ai-wont-replace-business-competitor-using-ai-will",
        "meta_title": "AI Automation for Small and Mid-Size Businesses",
        "meta_description": "A sober breakdown of where AI automation is actually producing ROI today: lead follow-ups, chatbots, inventory triggers, and workflow intelligence.",
        "keywords": "AI automation business, AI chatbots, lead follow-up automation, workflow automation, AI ROI",
        "image_id": "8386434",
        "intro": "The worst AI content makes two mistakes. It either claims AI will replace every business, or it dismisses AI as hype. Both positions are lazy. The more useful truth is that AI will not replace your business. But a competitor using AI to respond faster, personalize better, and operate with less waste might.",
        "howtos": [
            ("Start with repetitive work", "Identify tasks that repeat daily and follow predictable rules."),
            ("Automate response speed", "Use AI or workflow tools to answer, route, and qualify leads faster."),
            ("Connect AI to real data", "Avoid standalone toys. Automation works best when connected to CRM, inventory, or support systems."),
            ("Measure before expanding", "Track time saved, response time, conversion impact, and error reduction."),
        ],
        "faqs": [
            ("Where does AI create ROI fastest?", "Lead response, support triage, follow-up drafting, internal search, and operational alerts are common starting points."),
            ("Do small businesses need AI?", "They need useful automation. AI is valuable when it solves a clear workflow problem."),
            ("What should businesses avoid?", "Avoid AI tools that are impressive in demos but disconnected from real data or team behavior."),
        ],
    },
    {
        "category": "Research",
        "title": "We Audited 20 Indian E-Commerce Stores. Here's What We Found.",
        "slug": "audited-20-indian-ecommerce-stores",
        "meta_title": "20 Indian E-Commerce Stores Audited: What We Found",
        "meta_description": "A research-style breakdown of common e-commerce issues: plugin overload, slow pages, redundant tools, and weak conversion infrastructure.",
        "keywords": "Indian e-commerce audit, store speed audit, plugin audit, e-commerce benchmark, website performance India",
        "image_id": "590022",
        "intro": "When you audit enough e-commerce stores, the patterns stop feeling accidental. Different industries, different founders, different catalog sizes, but the same problems keep appearing: too many tools, slow storefronts, unclear ownership, weak tracking, and backend workflows held together by manual effort.",
        "howtos": [
            ("Score plugin dependency", "Count paid tools, duplicated tools, and tools that affect page load."),
            ("Measure key pages", "Check homepage, product page, collection page, cart, and checkout speed."),
            ("Inspect conversion clarity", "Review whether the visitor has one obvious next action per page."),
            ("Benchmark operations", "Assess inventory accuracy, CRM usage, follow-up speed, and analytics reliability."),
        ],
        "faqs": [
            ("What should an e-commerce audit include?", "Performance, plugin cost, UX clarity, checkout friction, tracking quality, and operational workflows."),
            ("How often should stores be audited?", "Quarterly for growing stores, and before major campaigns or seasonal peaks."),
            ("What is the most common issue?", "Tool overload combined with slow performance and unclear ownership."),
        ],
    },
    {
        "category": "Performance",
        "title": "The Real Cost of a Slow Website — A Number Most Founders Have Never Calculated",
        "slug": "real-cost-of-slow-website-founders-never-calculated",
        "meta_title": "The Real Revenue Cost of a Slow Website",
        "meta_description": "A practical framework for calculating how slow load times quietly reduce conversions, revenue, and marketing efficiency.",
        "keywords": "slow website cost, page speed revenue loss, conversion rate optimization, website performance, e-commerce speed",
        "image_id": "669615",
        "intro": "Slow websites are usually discussed as a technical problem. They are not. They are a revenue problem wearing a technical costume. A founder may tolerate a three-second load time because the site still opens. Customers are less patient. Every extra second taxes attention, trust, and conversion intent.",
        "howtos": [
            ("Find current conversion rate", "Start with sessions, add-to-cart, checkout, and purchase conversion data."),
            ("Measure page speed by page type", "Separate homepage, landing page, product page, and checkout performance."),
            ("Estimate lost conversion", "Model conservative drops from slow load time and compare against monthly revenue."),
            ("Prioritize high-value fixes", "Fix heavy scripts, uncompressed images, render-blocking code, and bloated tools first."),
        ],
        "faqs": [
            ("How much speed is good enough?", "For commerce pages, the closer to instant the better. Sub-2-second targets are a strong practical benchmark."),
            ("Does speed affect SEO?", "Yes. Performance influences user experience and can affect search visibility and engagement."),
            ("What usually slows websites down?", "Large images, excess JavaScript, plugin bloat, poor hosting, and unoptimized themes."),
        ],
    },
    {
        "category": "Indian Entrepreneurship",
        "title": "Why the Next Wave of Indian Entrepreneurs Will Win or Lose on Their Tech Stack",
        "slug": "next-wave-indian-entrepreneurs-win-or-lose-tech-stack",
        "meta_title": "Indian Entrepreneurs Will Win or Lose on Their Tech Stack",
        "meta_description": "A macro look at why digital infrastructure, not just funding and marketing, will define the next generation of Indian business winners.",
        "keywords": "Indian entrepreneurs, tech stack, digital backbone, business infrastructure India, startup technology",
        "image_id": "3184360",
        "intro": "India's entrepreneurial wave is usually described through funding, ambition, consumer demand, and digital adoption. All of that matters. But beneath the visible story is a quieter question: what are these businesses building on? The next generation of winners will not just market better. They will operate better because their tech stack lets them.",
        "howtos": [
            ("List critical systems", "Map the tools that run sales, operations, fulfillment, finance, and customer relationships."),
            ("Identify rented dependencies", "Separate tools that are convenient from tools that own core business logic."),
            ("Design for scale early", "Avoid decisions that work at 100 orders but collapse at 10,000."),
            ("Invest in data visibility", "Make sure founders can see the health of the business without manual reporting rituals."),
        ],
        "faqs": [
            ("Why does tech stack matter for entrepreneurs?", "It determines speed, visibility, cost structure, and the ability to scale without chaos."),
            ("Should early businesses build custom tools?", "Only where the workflow is strategic or recurring subscription dependence becomes costly."),
            ("What is a digital backbone?", "The integrated set of systems that connects acquisition, operations, customer data, and revenue decisions."),
        ],
    },
    {
        "category": "Tech Philosophy",
        "title": "The Quiet Advantage: Why Boring Tech Decisions Build Better Businesses",
        "slug": "quiet-advantage-boring-tech-decisions-build-better-businesses",
        "meta_title": "Why Boring Tech Decisions Build Better Businesses",
        "meta_description": "A Big Scoop Studio manifesto on lean, owned, maintainable technology choices that compound better than hype-driven stacks.",
        "keywords": "boring technology, maintainable systems, custom over subscription, owned tech stack, business technology strategy",
        "image_id": "3183197",
        "intro": "The technology world worships novelty. New frameworks, new tools, new dashboards, new promises. But the businesses that compound quietly often make the least dramatic decisions. They choose stable over fashionable, owned over rented, fast over fancy, and maintainable over impressive.",
        "howtos": [
            ("Choose boring where reliability matters", "Use proven architecture for revenue-critical workflows."),
            ("Own strategic logic", "Custom-build the systems that define your business advantage."),
            ("Avoid tool chasing", "Do not replace working systems only because a trend is louder."),
            ("Document and maintain", "A boring system becomes powerful when it can be understood, updated, and trusted."),
        ],
        "faqs": [
            ("Does boring technology mean outdated technology?", "No. It means proven, maintainable, and appropriate technology."),
            ("Why is owned technology an advantage?", "It reduces dependency and lets the business shape systems around its own operating model."),
            ("What is Big Scoop Studio's technology philosophy?", "Lean, fast, maintainable systems built around business outcomes rather than hype."),
        ],
    },
]


def pexels_url(photo_id):
    return f"https://images.pexels.com/photos/{photo_id}/pexels-photo-{photo_id}.jpeg?auto=compress&cs=tinysrgb&w=1800"


def download_image(photo_id):
    url = pexels_url(photo_id)
    request = Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urlopen(request, timeout=30) as response:
            return response.read(), url
    except (HTTPError, URLError, TimeoutError) as exc:
        print(f"Image download failed for Pexels photo {photo_id}: {exc}")
        return None, url


def fallback_image(title):
    image = Image.new("RGB", IMAGE_SIZE, "#f7f3f0")
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, IMAGE_SIZE[0], IMAGE_SIZE[1]), fill="#f7f3f0")
    draw.rectangle((80, 80, IMAGE_SIZE[0] - 80, IMAGE_SIZE[1] - 80), outline="#6F8F9F", width=6)
    draw.text((120, 380), "Big Scoop Studio", fill="#2E2E2E")
    draw.text((120, 430), title[:70], fill="#6F8F9F")
    buffer = BytesIO()
    image.save(buffer, format="JPEG", quality=95)
    return buffer.getvalue()


def save_webp_image(topic):
    image_bytes, source_url = download_image(topic["image_id"])
    if image_bytes is None:
        image_bytes = fallback_image(topic["title"])

    image = Image.open(BytesIO(image_bytes)).convert("RGB")
    image = ImageOps.fit(image, IMAGE_SIZE, method=Image.Resampling.LANCZOS, centering=(0.5, 0.5))

    banner_dir = Path(settings.MEDIA_ROOT) / "articles" / "banner"
    thumb_dir = Path(settings.MEDIA_ROOT) / "articles" / "thumbnail"
    banner_dir.mkdir(parents=True, exist_ok=True)
    thumb_dir.mkdir(parents=True, exist_ok=True)

    banner_path = banner_dir / f"{topic['slug']}.webp"
    thumb_path = thumb_dir / f"{topic['slug']}.webp"

    image.save(banner_path, "WEBP", quality=88, method=6)
    image.save(thumb_path, "WEBP", quality=88, method=6)

    return (
        f"articles/banner/{topic['slug']}.webp",
        f"articles/thumbnail/{topic['slug']}.webp",
        source_url,
    )


def get_author():
    user = (
        User.objects.filter(role="master").first()
        or User.objects.filter(is_superuser=True).first()
        or User.objects.first()
    )
    if not user:
        user = User.objects.create_user(
            username="big-scoop-editor",
            email="ceo@bigscoopstudio.com",
            password=None,
            role="master",
            first_name="Big Scoop",
            last_name="Studio",
        )
    return Author.objects.get_or_create(user=user)[0]


def seed():
    author = get_author()
    created_count = 0
    updated_count = 0

    for topic in TOPICS:
        category, _ = Category.objects.get_or_create(
            slug=topic["category"].lower().replace(" ", "-"),
            defaults={"name": topic["category"]},
        )

        banner_path, thumbnail_path, source_url = save_webp_image(topic)
        description = build_article(topic)

        article, created = Article.objects.update_or_create(
            slug=topic["slug"],
            defaults={
                "author": author,
                "category": category,
                "title": topic["title"],
                "meta_title": topic["meta_title"],
                "meta_description": topic["meta_description"],
                "keywords": topic["keywords"],
                "description": description,
                "banner_image": banner_path,
                "thumbnail_image": thumbnail_path,
                "is_published": True,
            },
        )

        ArticleFAQ.objects.filter(article=article).delete()
        ArticleHowTo.objects.filter(article=article).delete()

        for faq in topic["faqs"]:
            ArticleFAQ.objects.create(article=article, question=faq[0], answer=faq[1])

        for order, howto in enumerate(topic["howtos"], start=1):
            ArticleHowTo.objects.create(
                article=article,
                step_title=howto[0],
                step_description=howto[1],
                order=order,
            )

        if created:
            created_count += 1
        else:
            updated_count += 1

        print(f"{'Created' if created else 'Updated'}: {article.slug} ({words(description)} words) | image: {source_url}")

    print(f"Done. Created {created_count}, updated {updated_count}.")


if __name__ == "__main__":
    seed()
