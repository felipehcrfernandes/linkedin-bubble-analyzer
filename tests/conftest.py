import pytest


@pytest.fixture
def sample_posts():
    return [
        {
            "author": "Alice Johnson",
            "content": "Excited to share that our AI startup just closed a $10M Series A! "
            "The future of machine learning in healthcare is bright. #AI #startup #healthcare",
            "date": "2024-01-15",
            "likes": 234,
            "comments": 45,
        },
        {
            "author": "Bob Smith",
            "content": "Just published my thoughts on why every developer should learn Rust. "
            "Memory safety without garbage collection is a game changer. "
            "Check out the full article on my blog.",
            "date": "2024-01-14",
            "likes": 189,
            "comments": 67,
        },
        {
            "author": "Carol Davis",
            "content": "Our team just shipped a new feature using React Server Components. "
            "The performance improvements are incredible - 40% faster page loads! "
            "#webdev #react #performance",
            "date": "2024-01-13",
            "likes": 156,
            "comments": 23,
        },
        {
            "author": "David Lee",
            "content": "Hot take: The best programming language is the one that solves your problem. "
            "Stop arguing about languages and start building things.",
            "date": "2024-01-12",
            "likes": 445,
            "comments": 122,
        },
        {
            "author": "Eve Wilson",
            "content": "AI is transforming healthcare diagnostics. Our latest model achieves "
            "95% accuracy in early cancer detection. This is what technology should be about. "
            "#AI #healthcare #deeplearning",
            "date": "2024-01-11",
            "likes": 567,
            "comments": 89,
        },
        {
            "author": "Frank Brown",
            "content": "Excited to announce our AI-powered drug discovery platform! "
            "Machine learning is revolutionizing how we find new treatments. "
            "#AI #healthcare #biotech",
            "date": "2024-01-10",
            "likes": 312,
            "comments": 56,
        },
        {
            "author": "Grace Chen",
            "content": "5 tips for landing your first tech job: "
            "1. Build projects 2. Contribute to open source 3. Network "
            "4. Practice interviews 5. Never stop learning. #career #tech",
            "date": "2024-01-09",
            "likes": 678,
            "comments": 145,
        },
        {
            "author": "Henry Taylor",
            "content": "The Rust programming language continues to grow. "
            "Memory safety, performance, and a great community. "
            "Why more companies are adopting Rust in 2024.",
            "date": "2024-01-08",
            "likes": 234,
            "comments": 78,
        },
        {
            "author": "Ivy Martinez",
            "content": "React vs Vue vs Angular - the eternal debate. "
            "But honestly, all three are great frameworks. "
            "Choose based on your team and project needs. #webdev #frontend",
            "date": "2024-01-07",
            "likes": 189,
            "comments": 91,
        },
        {
            "author": "Jack Robinson",
            "content": "Leadership in tech isn't about having all the answers. "
            "It's about asking the right questions and empowering your team. "
            "#leadership #management #tech",
            "date": "2024-01-06",
            "likes": 345,
            "comments": 34,
        },
    ]
