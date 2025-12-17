"""
Management command to create test data for the journal
Creates articles, book reviews, and movie reviews with realistic content
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from accounts.models import Author
from articles.models import Article, Category, Tag
from reviews.models import BookReview, MovieReview, BookCategory, MovieCategory
from datetime import timedelta
import random

User = get_user_model()


class Command(BaseCommand):
    help = 'Create test data: 20 articles, 10 book reviews, 15 movie reviews'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing test data before creating new',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write(self.style.WARNING('Clearing existing data...'))
            Article.objects.all().delete()
            BookReview.objects.all().delete()
            MovieReview.objects.all().delete()
            Category.objects.all().delete()
            Tag.objects.all().delete()
            BookCategory.objects.all().delete()
            MovieCategory.objects.all().delete()
            # Delete test author if exists
            Author.objects.filter(slug='parsa-journalist').delete()

        # Create or get author
        author = self.get_or_create_author()
        
        # Create categories
        article_categories = self.create_article_categories()
        book_categories = self.create_book_categories()
        movie_categories = self.create_movie_categories()
        
        # Create tags
        tags = self.create_tags()
        
        # Create articles
        self.stdout.write(self.style.SUCCESS('Creating 20 English articles...'))
        self.create_articles(author, article_categories, tags, language='en')
        
        self.stdout.write(self.style.SUCCESS('Creating 15 Persian articles...'))
        self.create_persian_articles(author, article_categories, tags)
        
        # Create book reviews
        self.stdout.write(self.style.SUCCESS('Creating 10 book reviews...'))
        self.create_book_reviews(author, book_categories)
        
        self.stdout.write(self.style.SUCCESS('Creating 6 Persian book reviews...'))
        self.create_persian_book_reviews(author, book_categories)
        
        # Create movie reviews
        self.stdout.write(self.style.SUCCESS('Creating 15 movie reviews...'))
        self.create_movie_reviews(author, movie_categories)
        
        self.stdout.write(self.style.SUCCESS('Creating 6 Persian movie reviews...'))
        self.create_persian_movie_reviews(author, movie_categories)
        
        self.stdout.write(self.style.SUCCESS('\n✅ Test data created successfully!'))
        self.stdout.write(f'   - Articles: {Article.objects.count()}')
        self.stdout.write(f'   - Book Reviews: {BookReview.objects.count()}')
        self.stdout.write(f'   - Movie Reviews: {MovieReview.objects.count()}')

    def get_or_create_author(self):
        """Get or create an author"""
        # Try to get existing author by slug first
        try:
            author = Author.objects.get(slug='parsa-journalist')
            self.stdout.write(self.style.SUCCESS(f'Using existing author: {author.display_name}'))
            return author
        except Author.DoesNotExist:
            pass
        
        # Get or create user
        user = User.objects.first()
        if not user:
            user = User.objects.create_user(
                username='test_author',
                email='author@test.com',
                password='testpass123'
            )
        
        # Create author
        author = Author.objects.create(
            user=user,
            display_name='Parsa Journalist',
            slug='parsa-journalist',
            bio='A passionate journalist and reviewer with years of experience in writing and critiquing.',
            is_active=True
        )
        
        self.stdout.write(self.style.SUCCESS(f'Created author: {author.display_name}'))
        return author

    def create_article_categories(self):
        """Create article categories"""
        categories_data = [
            {'name': 'Technology', 'description': 'Latest technology news and insights'},
            {'name': 'Culture', 'description': 'Cultural articles and analysis'},
            {'name': 'Politics', 'description': 'Political commentary and news'},
            {'name': 'Society', 'description': 'Social issues and discussions'},
            {'name': 'Science', 'description': 'Scientific discoveries and research'},
        ]
        
        categories = []
        for cat_data in categories_data:
            cat, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            categories.append(cat)
        
        return categories

    def create_book_categories(self):
        """Create book categories"""
        categories_data = [
            {'name': 'Fiction', 'description': 'Fictional books and novels'},
            {'name': 'Non-Fiction', 'description': 'Non-fiction books and biographies'},
            {'name': 'Science Fiction', 'description': 'Sci-fi and fantasy books'},
            {'name': 'History', 'description': 'Historical books and accounts'},
        ]
        
        categories = []
        for cat_data in categories_data:
            cat, created = BookCategory.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            categories.append(cat)
        
        return categories

    def create_movie_categories(self):
        """Create movie categories"""
        categories_data = [
            {'name': 'Drama', 'description': 'Dramatic films and stories'},
            {'name': 'Action', 'description': 'Action and adventure movies'},
            {'name': 'Comedy', 'description': 'Comedy films'},
            {'name': 'Thriller', 'description': 'Thriller and suspense movies'},
            {'name': 'Documentary', 'description': 'Documentary films'},
        ]
        
        categories = []
        for cat_data in categories_data:
            cat, created = MovieCategory.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            categories.append(cat)
        
        return categories

    def create_tags(self):
        """Create article tags"""
        tag_names = [
            'Technology', 'AI', 'Innovation', 'Culture', 'Politics',
            'Society', 'Science', 'Health', 'Education', 'Environment',
            'Business', 'Economy', 'Art', 'Literature', 'History'
        ]
        
        tags = []
        for tag_name in tag_names:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            tags.append(tag)
        
        return tags

    def create_articles(self, author, categories, tags, language='en'):
        """Create test articles"""
        articles_data = [
            {
                'title': 'The Future of Artificial Intelligence in Journalism',
                'excerpt': 'Exploring how AI is transforming the way we consume and produce news content.',
                'content': '<p>Artificial Intelligence is revolutionizing journalism in unprecedented ways. From automated news writing to personalized content delivery, AI technologies are reshaping the media landscape.</p><p>News organizations are increasingly adopting AI tools to enhance their reporting capabilities, analyze vast amounts of data, and deliver more relevant content to their audiences.</p><p>However, this transformation also raises important questions about journalistic integrity, bias, and the future role of human journalists in an AI-driven world.</p>',
                'category': 'Technology',
                'tags': ['Technology', 'AI', 'Innovation'],
                'is_featured': True
            },
            {
                'title': 'Climate Change: The Urgent Call for Action',
                'excerpt': 'An in-depth analysis of climate change impacts and the necessary steps for mitigation.',
                'content': '<p>Climate change represents one of the most pressing challenges of our time. Rising global temperatures, extreme weather events, and environmental degradation demand immediate and coordinated action.</p><p>Scientists worldwide are calling for urgent measures to reduce greenhouse gas emissions and transition to sustainable energy sources.</p><p>The window for meaningful action is closing rapidly, making it imperative for governments, businesses, and individuals to work together towards a sustainable future.</p>',
                'category': 'Science',
                'tags': ['Science', 'Environment', 'Society'],
                'is_featured': True
            },
            {
                'title': 'The Evolution of Social Media and Its Impact on Society',
                'excerpt': 'How social media platforms have changed the way we communicate and interact.',
                'content': '<p>Social media has fundamentally altered human communication and social interaction. Platforms like Facebook, Twitter, and Instagram have created new ways for people to connect, share information, and express themselves.</p><p>While these platforms offer unprecedented opportunities for connection and information sharing, they also present challenges including privacy concerns, misinformation, and mental health impacts.</p><p>Understanding the complex relationship between social media and society is crucial for navigating the digital age effectively.</p>',
                'category': 'Society',
                'tags': ['Society', 'Technology', 'Culture'],
                'is_featured': False
            },
            {
                'title': 'Democracy in the Digital Age: Challenges and Opportunities',
                'excerpt': 'Examining how digital technologies are reshaping democratic processes worldwide.',
                'content': '<p>Digital technologies are transforming democratic institutions and processes in profound ways. Online voting, digital campaigning, and social media engagement have become integral parts of modern democracy.</p><p>However, these technologies also introduce new challenges including cybersecurity threats, misinformation campaigns, and digital divides that can undermine democratic participation.</p><p>Balancing the opportunities and risks of digital democracy requires careful consideration of technology, policy, and civic engagement.</p>',
                'category': 'Politics',
                'tags': ['Politics', 'Technology', 'Society'],
                'is_featured': False
            },
            {
                'title': 'The Renaissance of Independent Journalism',
                'excerpt': 'How independent journalists are reshaping media in the age of digital platforms.',
                'content': '<p>Independent journalism is experiencing a renaissance as digital platforms enable individual journalists to reach global audiences without traditional media gatekeepers.</p><p>This shift has democratized media production but also raised questions about journalistic standards, fact-checking, and sustainable business models.</p><p>Independent journalists are finding innovative ways to fund their work while maintaining editorial independence and journalistic integrity.</p>',
                'category': 'Culture',
                'tags': ['Culture', 'Society', 'Business'],
                'is_featured': False
            },
            {
                'title': 'Quantum Computing: Breaking Barriers in Technology',
                'excerpt': 'Understanding the revolutionary potential of quantum computing and its applications.',
                'content': '<p>Quantum computing represents a paradigm shift in computational power, promising to solve problems that are currently intractable for classical computers.</p><p>From cryptography to drug discovery, quantum computers have the potential to revolutionize numerous fields and industries.</p><p>While still in early stages, significant progress is being made in developing practical quantum computing systems that could transform technology as we know it.</p>',
                'category': 'Technology',
                'tags': ['Technology', 'Science', 'Innovation'],
                'is_featured': False
            },
            {
                'title': 'Cultural Heritage in the Modern World',
                'excerpt': 'Preserving and celebrating cultural heritage in an increasingly globalized world.',
                'content': '<p>Cultural heritage represents the accumulated knowledge, traditions, and artifacts that define human civilization. In our globalized world, preserving this heritage while allowing for cultural exchange presents unique challenges.</p><p>Digital technologies offer new opportunities for documenting, preserving, and sharing cultural heritage with global audiences.</p><p>Balancing preservation with accessibility requires careful consideration of cultural sensitivity, ownership, and the evolving nature of cultural expression.</p>',
                'category': 'Culture',
                'tags': ['Culture', 'History', 'Society'],
                'is_featured': False
            },
            {
                'title': 'The Economics of Sustainable Development',
                'excerpt': 'Analyzing economic models that prioritize environmental sustainability and social equity.',
                'content': '<p>Sustainable development requires rethinking traditional economic models to prioritize long-term environmental health and social equity alongside economic growth.</p><p>Green economies, circular business models, and impact investing are emerging as key strategies for achieving sustainable development goals.</p><p>The transition to sustainable economic systems presents both challenges and opportunities for businesses, governments, and communities worldwide.</p>',
                'category': 'Society',
                'tags': ['Economy', 'Environment', 'Business'],
                'is_featured': False
            },
            {
                'title': 'Mental Health Awareness in Contemporary Society',
                'excerpt': 'The growing importance of mental health awareness and support systems.',
                'content': '<p>Mental health awareness has gained significant traction in recent years, breaking down stigmas and encouraging open conversations about psychological well-being.</p><p>Access to mental health services, workplace mental health programs, and community support systems are becoming increasingly important.</p><p>Addressing mental health challenges requires comprehensive approaches that consider individual, social, and systemic factors.</p>',
                'category': 'Society',
                'tags': ['Health', 'Society'],
                'is_featured': False
            },
            {
                'title': 'The Art of Storytelling in Digital Media',
                'excerpt': 'How digital platforms are transforming the ancient art of storytelling.',
                'content': '<p>Storytelling has evolved dramatically with the advent of digital media, offering new formats, platforms, and interactive possibilities.</p><p>From podcasts to interactive documentaries, digital storytelling enables creators to engage audiences in innovative and immersive ways.</p><p>The fundamental principles of good storytelling remain constant, but digital tools provide unprecedented opportunities for creative expression and audience engagement.</p>',
                'category': 'Culture',
                'tags': ['Culture', 'Art', 'Technology'],
                'is_featured': False
            },
            {
                'title': 'Space Exploration: The Next Frontier',
                'excerpt': 'Recent developments in space exploration and their implications for humanity.',
                'content': '<p>Space exploration is entering an exciting new era with private companies joining government agencies in pushing the boundaries of human spaceflight.</p><p>Mars missions, asteroid mining, and space tourism represent just a few of the ambitious projects underway.</p><p>These developments raise important questions about space governance, resource allocation, and the future of human presence beyond Earth.</p>',
                'category': 'Science',
                'tags': ['Science', 'Technology', 'Innovation'],
                'is_featured': False
            },
            {
                'title': 'Education Reform in the 21st Century',
                'excerpt': 'Reimagining education systems to meet the challenges of the modern world.',
                'content': '<p>Education systems worldwide are undergoing significant reforms to better prepare students for rapidly changing economic and social landscapes.</p><p>Emphasis on critical thinking, digital literacy, and adaptability is replacing traditional rote learning approaches.</p><p>Technology integration, personalized learning, and skills-based curricula are becoming central to modern educational strategies.</p>',
                'category': 'Society',
                'tags': ['Education', 'Society', 'Technology'],
                'is_featured': False
            },
            {
                'title': 'The Power of Local Journalism',
                'excerpt': 'Why local journalism matters more than ever in the digital age.',
                'content': '<p>Local journalism plays a crucial role in holding power accountable and keeping communities informed about issues that directly affect their daily lives.</p><p>Despite challenges from digital disruption, local news organizations continue to provide essential coverage of local government, schools, and community events.</p><p>Supporting local journalism is essential for maintaining informed, engaged, and democratic communities.</p>',
                'category': 'Culture',
                'tags': ['Culture', 'Society', 'Politics'],
                'is_featured': False
            },
            {
                'title': 'Biotechnology Breakthroughs and Ethical Considerations',
                'excerpt': 'Recent advances in biotechnology and the ethical questions they raise.',
                'content': '<p>Biotechnology is advancing at an unprecedented pace, with breakthroughs in gene editing, synthetic biology, and personalized medicine.</p><p>These advances offer tremendous potential for treating diseases and improving human health, but also raise complex ethical questions.</p><p>Balancing scientific progress with ethical considerations requires ongoing dialogue between scientists, ethicists, policymakers, and the public.</p>',
                'category': 'Science',
                'tags': ['Science', 'Health', 'Innovation'],
                'is_featured': False
            },
            {
                'title': 'Urban Planning for Sustainable Cities',
                'excerpt': 'Designing cities that are both livable and environmentally sustainable.',
                'content': '<p>As urban populations continue to grow, sustainable urban planning becomes increasingly critical for creating livable, environmentally responsible cities.</p><p>Green infrastructure, public transportation, and mixed-use development are key strategies for sustainable urban design.</p><p>Successful sustainable cities balance economic development, environmental protection, and social equity to create thriving communities.</p>',
                'category': 'Society',
                'tags': ['Environment', 'Society', 'Business'],
                'is_featured': False
            },
            {
                'title': 'The Intersection of Art and Technology',
                'excerpt': 'How technology is expanding the boundaries of artistic expression.',
                'content': '<p>Technology is opening new frontiers for artistic expression, enabling creators to explore innovative forms and engage audiences in unprecedented ways.</p><p>Digital art, virtual reality experiences, and AI-generated content are challenging traditional notions of art and creativity.</p><p>The fusion of art and technology creates exciting possibilities while also raising questions about authenticity, authorship, and the nature of creativity.</p>',
                'category': 'Culture',
                'tags': ['Art', 'Technology', 'Culture'],
                'is_featured': False
            },
            {
                'title': 'Global Migration Patterns and Their Impact',
                'excerpt': 'Understanding contemporary migration trends and their social implications.',
                'content': '<p>Global migration patterns are reshaping societies worldwide, driven by economic opportunities, conflict, and environmental factors.</p><p>Migration brings both challenges and opportunities for host communities, requiring thoughtful policies and integration strategies.</p><p>Understanding migration dynamics is essential for creating inclusive, prosperous societies that benefit from diverse populations.</p>',
                'category': 'Society',
                'tags': ['Society', 'Politics', 'Economy'],
                'is_featured': False
            },
            {
                'title': 'The Future of Work in an Automated World',
                'excerpt': 'How automation and AI are transforming employment and the workplace.',
                'content': '<p>Automation and artificial intelligence are fundamentally transforming the nature of work, creating both opportunities and challenges for workers and employers.</p><p>While some jobs may be displaced, new roles are emerging that require human creativity, emotional intelligence, and complex problem-solving skills.</p><p>Preparing for the future of work requires investment in education, retraining programs, and social safety nets to support workers through transitions.</p>',
                'category': 'Technology',
                'tags': ['Technology', 'Economy', 'Business'],
                'is_featured': False
            },
            {
                'title': 'Preserving Indigenous Languages and Cultures',
                'excerpt': 'Efforts to protect and revitalize indigenous languages and cultural practices.',
                'content': '<p>Indigenous languages and cultures face ongoing threats from globalization, but dedicated efforts are underway to preserve and revitalize these invaluable cultural resources.</p><p>Language preservation programs, cultural education initiatives, and digital documentation projects are helping to maintain indigenous knowledge and traditions.</p><p>Supporting indigenous communities in preserving their languages and cultures is essential for maintaining global cultural diversity and heritage.</p>',
                'category': 'Culture',
                'tags': ['Culture', 'History', 'Society'],
                'is_featured': False
            },
            {
                'title': 'Cybersecurity in an Interconnected World',
                'excerpt': 'The critical importance of cybersecurity in protecting digital infrastructure.',
                'content': '<p>As our world becomes increasingly interconnected, cybersecurity has become a critical concern for individuals, businesses, and governments alike.</p><p>Cyber threats are evolving rapidly, requiring constant vigilance and adaptation of security measures.</p><p>Building robust cybersecurity requires collaboration between technology companies, governments, and users to create a safer digital environment for everyone.</p>',
                'category': 'Technology',
                'tags': ['Technology', 'Business', 'Politics'],
                'is_featured': False
            },
        ]
        
        base_date = timezone.now()
        for i, article_data in enumerate(articles_data):
            category = next((c for c in categories if c.name == article_data['category']), categories[0])
            article_tags = [t for t in tags if t.name in article_data['tags']]
            
            # Create article without image first (we'll handle images separately)
            article = Article.objects.create(
                title=article_data['title'],
                slug=slugify(article_data['title'], allow_unicode=True),
                author=author,
                category=category,
                excerpt=article_data['excerpt'],
                content=article_data['content'],
                status='published',
                is_featured=article_data.get('is_featured', False),
                published_at=base_date - timedelta(days=i),
                views=random.randint(10, 500),
                language=language
            )
            
            # Add tags
            article.tags.set(article_tags)
            
            self.stdout.write(f'  ✓ Created: {article.title}')

    def create_persian_articles(self, author, categories, tags):
        """Create 15 Persian test articles"""
        persian_articles_data = [
            {
                'title': 'آینده هوش مصنوعی در روزنامه‌نگاری',
                'excerpt': 'بررسی چگونگی تحول هوش مصنوعی در نحوه تولید و مصرف محتوای خبری.',
                'content': '<p>هوش مصنوعی به روش‌های بی‌سابقه‌ای در حال تحول روزنامه‌نگاری است. از نوشتن خودکار اخبار تا ارائه محتوای شخصی‌سازی شده، فناوری‌های هوش مصنوعی در حال تغییر چهره رسانه هستند.</p><p>سازمان‌های خبری به طور فزاینده‌ای از ابزارهای هوش مصنوعی برای بهبود قابلیت‌های گزارش‌دهی، تجزیه و تحلیل حجم عظیمی از داده‌ها و ارائه محتوای مرتبط‌تر به مخاطبان خود استفاده می‌کنند.</p><p>با این حال، این تحول سوالات مهمی را در مورد یکپارچگی روزنامه‌نگاری، تعصب و نقش آینده روزنامه‌نگاران انسانی در دنیای مبتنی بر هوش مصنوعی مطرح می‌کند.</p>',
                'category': 'Technology',
                'tags': ['Technology', 'AI', 'Innovation'],
                'is_featured': True
            },
            {
                'title': 'تغییرات اقلیمی: فراخوان فوری برای اقدام',
                'excerpt': 'تحلیل عمیق از تأثیرات تغییرات اقلیمی و اقدامات لازم برای کاهش آن.',
                'content': '<p>تغییرات اقلیمی یکی از چالش‌برانگیزترین مسائل زمان ماست. افزایش دمای جهانی، رویدادهای آب و هوایی شدید و تخریب محیط زیست نیاز به اقدام فوری و هماهنگ دارد.</p><p>دانشمندان در سراسر جهان خواستار اقدامات فوری برای کاهش انتشار گازهای گلخانه‌ای و انتقال به منابع انرژی پایدار هستند.</p><p>فرصت برای اقدام معنادار به سرعت در حال بسته شدن است و این امر ضروری می‌سازد که دولت‌ها، کسب‌وکارها و افراد با هم برای آینده‌ای پایدار تلاش کنند.</p>',
                'category': 'Science',
                'tags': ['Science', 'Environment', 'Society'],
                'is_featured': True
            },
            {
                'title': 'تکامل شبکه‌های اجتماعی و تأثیر آن بر جامعه',
                'excerpt': 'چگونگی تغییر پلتفرم‌های شبکه‌های اجتماعی در نحوه ارتباط و تعامل ما.',
                'content': '<p>شبکه‌های اجتماعی اساساً ارتباطات انسانی و تعاملات اجتماعی را تغییر داده‌اند. پلتفرم‌هایی مانند فیس‌بوک، توییتر و اینستاگرام روش‌های جدیدی برای ارتباط، اشتراک‌گذاری اطلاعات و بیان خود ایجاد کرده‌اند.</p><p>در حالی که این پلتفرم‌ها فرصت‌های بی‌سابقه‌ای برای ارتباط و اشتراک‌گذاری اطلاعات ارائه می‌دهند، چالش‌هایی از جمله نگرانی‌های حریم خصوصی، اطلاعات نادرست و تأثیرات سلامت روان را نیز به همراه دارند.</p><p>درک رابطه پیچیده بین شبکه‌های اجتماعی و جامعه برای حرکت مؤثر در عصر دیجیتال ضروری است.</p>',
                'category': 'Society',
                'tags': ['Society', 'Technology', 'Culture'],
                'is_featured': False
            },
            {
                'title': 'دموکراسی در عصر دیجیتال: چالش‌ها و فرصت‌ها',
                'excerpt': 'بررسی چگونگی تحول فناوری‌های دیجیتال در فرآیندهای دموکراتیک در سراسر جهان.',
                'content': '<p>فناوری‌های دیجیتال نهادها و فرآیندهای دموکراتیک را به روش‌های عمیقی در حال تحول هستند. رای‌گیری آنلاین، کمپین‌های دیجیتال و مشارکت در شبکه‌های اجتماعی به بخش‌های جدایی‌ناپذیر دموکراسی مدرن تبدیل شده‌اند.</p><p>با این حال، این فناوری‌ها چالش‌های جدیدی از جمله تهدیدات امنیت سایبری، کمپین‌های اطلاعات نادرست و شکاف‌های دیجیتالی که می‌توانند مشارکت دموکراتیک را تضعیف کنند، به همراه دارند.</p><p>تعادل بین فرصت‌ها و خطرات دموکراسی دیجیتال نیاز به بررسی دقیق فناوری، سیاست و مشارکت مدنی دارد.</p>',
                'category': 'Politics',
                'tags': ['Politics', 'Technology', 'Society'],
                'is_featured': False
            },
            {
                'title': 'رنسانس روزنامه‌نگاری مستقل',
                'excerpt': 'چگونگی تحول روزنامه‌نگاران مستقل در رسانه در عصر پلتفرم‌های دیجیتال.',
                'content': '<p>روزنامه‌نگاری مستقل در حال تجربه رنسانسی است که پلتفرم‌های دیجیتال به روزنامه‌نگاران فردی امکان دسترسی به مخاطبان جهانی بدون دروازه‌بان‌های رسانه‌ای سنتی را می‌دهند.</p><p>این تغییر تولید رسانه را دموکراتیک کرده است اما سوالاتی را در مورد استانداردهای روزنامه‌نگاری، بررسی واقعیت و مدل‌های تجاری پایدار مطرح کرده است.</p><p>روزنامه‌نگاران مستقل راه‌های نوآورانه‌ای برای تأمین مالی کار خود در حالی که استقلال تحریریه و یکپارچگی روزنامه‌نگاری را حفظ می‌کنند، پیدا می‌کنند.</p>',
                'category': 'Culture',
                'tags': ['Culture', 'Society', 'Business'],
                'is_featured': False
            },
            {
                'title': 'رایانش کوانتومی: شکستن موانع در فناوری',
                'excerpt': 'درک پتانسیل انقلابی رایانش کوانتومی و کاربردهای آن.',
                'content': '<p>رایانش کوانتومی نشان‌دهنده تغییر پارادایم در قدرت محاسباتی است که وعده حل مسائلی را می‌دهد که در حال حاضر برای رایانه‌های کلاسیک غیرقابل حل هستند.</p><p>از رمزنگاری تا کشف دارو، رایانه‌های کوانتومی پتانسیل تحول در زمینه‌ها و صنایع متعددی را دارند.</p><p>در حالی که هنوز در مراحل اولیه است، پیشرفت قابل توجهی در توسعه سیستم‌های رایانش کوانتومی عملی که می‌توانند فناوری را همانطور که می‌شناسیم متحول کنند، در حال انجام است.</p>',
                'category': 'Technology',
                'tags': ['Technology', 'Science', 'Innovation'],
                'is_featured': False
            },
            {
                'title': 'میراث فرهنگی در جهان مدرن',
                'excerpt': 'حفظ و جشن گرفتن میراث فرهنگی در جهانی که به طور فزاینده‌ای جهانی‌شده است.',
                'content': '<p>میراث فرهنگی نشان‌دهنده دانش، سنت‌ها و آثار انباشته‌ای است که تمدن بشری را تعریف می‌کند. در جهان جهانی‌شده ما، حفظ این میراث در حالی که امکان تبادل فرهنگی را فراهم می‌کند، چالش‌های منحصر به فردی را ارائه می‌دهد.</p><p>فناوری‌های دیجیتال فرصت‌های جدیدی برای مستندسازی، حفظ و اشتراک‌گذاری میراث فرهنگی با مخاطبان جهانی ارائه می‌دهند.</p><p>تعادل بین حفظ و دسترسی نیاز به بررسی دقیق حساسیت فرهنگی، مالکیت و ماهیت در حال تحول بیان فرهنگی دارد.</p>',
                'category': 'Culture',
                'tags': ['Culture', 'History', 'Society'],
                'is_featured': False
            },
            {
                'title': 'اقتصاد توسعه پایدار',
                'excerpt': 'تحلیل مدل‌های اقتصادی که پایداری محیطی و برابری اجتماعی را در اولویت قرار می‌دهند.',
                'content': '<p>توسعه پایدار نیاز به بازنگری مدل‌های اقتصادی سنتی برای اولویت‌بندی سلامت محیطی بلندمدت و برابری اجتماعی در کنار رشد اقتصادی دارد.</p><p>اقتصادهای سبز، مدل‌های تجاری دایره‌ای و سرمایه‌گذاری تأثیرگذار به عنوان استراتژی‌های کلیدی برای دستیابی به اهداف توسعه پایدار در حال ظهور هستند.</p><p>انتقال به سیستم‌های اقتصادی پایدار هم چالش‌ها و هم فرصت‌هایی را برای کسب‌وکارها، دولت‌ها و جوامع در سراسر جهان ارائه می‌دهد.</p>',
                'category': 'Society',
                'tags': ['Economy', 'Environment', 'Business'],
                'is_featured': False
            },
            {
                'title': 'آگاهی از سلامت روان در جامعه معاصر',
                'excerpt': 'اهمیت فزاینده آگاهی از سلامت روان و سیستم‌های پشتیبانی.',
                'content': '<p>آگاهی از سلامت روان در سال‌های اخیر توجه قابل توجهی به خود جلب کرده است و با شکستن انگ‌ها و تشویق به گفتگوهای باز در مورد رفاه روانی همراه است.</p><p>دسترسی به خدمات سلامت روان، برنامه‌های سلامت روان در محل کار و سیستم‌های پشتیبانی جامعه به طور فزاینده‌ای مهم می‌شوند.</p><p>رسیدگی به چالش‌های سلامت روان نیاز به رویکردهای جامعی دارد که عوامل فردی، اجتماعی و سیستمیک را در نظر می‌گیرند.</p>',
                'category': 'Society',
                'tags': ['Health', 'Society'],
                'is_featured': False
            },
            {
                'title': 'هنر داستان‌سرایی در رسانه دیجیتال',
                'excerpt': 'چگونگی تحول پلتفرم‌های دیجیتال در هنر باستانی داستان‌سرایی.',
                'content': '<p>داستان‌سرایی با ظهور رسانه دیجیتال به طور چشمگیری تکامل یافته است و فرمت‌ها، پلتفرم‌ها و امکانات تعاملی جدیدی را ارائه می‌دهد.</p><p>از پادکست‌ها تا مستندهای تعاملی، داستان‌سرایی دیجیتال به خالقان امکان درگیر کردن مخاطبان به روش‌های نوآورانه و جذاب را می‌دهد.</p><p>اصول اساسی داستان‌سرایی خوب ثابت می‌ماند، اما ابزارهای دیجیتال فرصت‌های بی‌سابقه‌ای برای بیان خلاقانه و درگیری مخاطب ارائه می‌دهند.</p>',
                'category': 'Culture',
                'tags': ['Culture', 'Art', 'Technology'],
                'is_featured': False
            },
            {
                'title': 'اکتشاف فضا: مرز بعدی',
                'excerpt': 'توسعه‌های اخیر در اکتشاف فضا و پیامدهای آن برای بشریت.',
                'content': '<p>اکتشاف فضا در حال ورود به عصر هیجان‌انگیز جدیدی است که شرکت‌های خصوصی به آژانس‌های دولتی در پیشبرد مرزهای پرواز فضایی انسانی می‌پیوندند.</p><p>ماموریت‌های مریخ، استخراج سیارک‌ها و گردشگری فضایی تنها چند مورد از پروژه‌های بلندپروازانه در حال انجام هستند.</p><p>این توسعه‌ها سوالات مهمی را در مورد حکمرانی فضا، تخصیص منابع و آینده حضور انسانی فراتر از زمین مطرح می‌کند.</p>',
                'category': 'Science',
                'tags': ['Science', 'Technology', 'Innovation'],
                'is_featured': False
            },
            {
                'title': 'اصلاح آموزش در قرن بیست و یکم',
                'excerpt': 'بازتصور سیستم‌های آموزشی برای پاسخگویی به چالش‌های جهان مدرن.',
                'content': '<p>سیستم‌های آموزشی در سراسر جهان در حال دستخوش اصلاحات قابل توجهی برای آماده‌سازی بهتر دانش‌آموزان برای مناظر اقتصادی و اجتماعی در حال تغییر سریع هستند.</p><p>تأکید بر تفکر انتقادی، سواد دیجیتال و سازگاری در حال جایگزینی رویکردهای یادگیری طوطی‌وار سنتی است.</p><p>ادغام فناوری، یادگیری شخصی‌سازی شده و برنامه‌های درسی مبتنی بر مهارت در حال تبدیل شدن به مرکز استراتژی‌های آموزشی مدرن هستند.</p>',
                'category': 'Society',
                'tags': ['Education', 'Society', 'Technology'],
                'is_featured': False
            },
            {
                'title': 'قدرت روزنامه‌نگاری محلی',
                'excerpt': 'چرا روزنامه‌نگاری محلی در عصر دیجیتال بیش از هر زمان دیگری مهم است.',
                'content': '<p>روزنامه‌نگاری محلی نقش مهمی در پاسخگو نگه داشتن قدرت و اطلاع‌رسانی به جوامع در مورد مسائلی که مستقیماً بر زندگی روزمره آن‌ها تأثیر می‌گذارد، ایفا می‌کند.</p><p>علیرغم چالش‌های ناشی از اختلال دیجیتال، سازمان‌های خبری محلی همچنان پوشش ضروری از دولت محلی، مدارس و رویدادهای جامعه را ارائه می‌دهند.</p><p>پشتیبانی از روزنامه‌نگاری محلی برای حفظ جوامع آگاه، درگیر و دموکراتیک ضروری است.</p>',
                'category': 'Culture',
                'tags': ['Culture', 'Society', 'Politics'],
                'is_featured': False
            },
            {
                'title': 'دستاوردهای بیوتکنولوژی و ملاحظات اخلاقی',
                'excerpt': 'پیشرفت‌های اخیر در بیوتکنولوژی و سوالات اخلاقی که مطرح می‌کند.',
                'content': '<p>بیوتکنولوژی با سرعتی بی‌سابقه در حال پیشرفت است و دستاوردهایی در ویرایش ژن، زیست‌شناسی مصنوعی و پزشکی شخصی‌سازی شده دارد.</p><p>این پیشرفت‌ها پتانسیل عظیمی برای درمان بیماری‌ها و بهبود سلامت انسان ارائه می‌دهند، اما سوالات پیچیده اخلاقی را نیز مطرح می‌کنند.</p><p>تعادل بین پیشرفت علمی و ملاحظات اخلاقی نیاز به گفتگوی مداوم بین دانشمندان، اخلاق‌شناسان، سیاست‌گذاران و عموم مردم دارد.</p>',
                'category': 'Science',
                'tags': ['Science', 'Health', 'Innovation'],
                'is_featured': False
            },
            {
                'title': 'برنامه‌ریزی شهری برای شهرهای پایدار',
                'excerpt': 'طراحی شهرهایی که هم قابل زندگی و هم از نظر محیطی پایدار هستند.',
                'content': '<p>با ادامه رشد جمعیت شهری، برنامه‌ریزی شهری پایدار برای ایجاد شهرهای قابل زندگی و مسئول از نظر محیطی به طور فزاینده‌ای مهم می‌شود.</p><p>زیرساخت‌های سبز، حمل و نقل عمومی و توسعه کاربری مختلط استراتژی‌های کلیدی برای طراحی شهری پایدار هستند.</p><p>شهرهای پایدار موفق تعادل بین توسعه اقتصادی، حفاظت از محیط زیست و برابری اجتماعی را برای ایجاد جوامع پررونق برقرار می‌کنند.</p>',
                'category': 'Society',
                'tags': ['Environment', 'Society', 'Business'],
                'is_featured': False
            },
        ]
        
        base_date = timezone.now()
        for i, article_data in enumerate(persian_articles_data):
            category = next((c for c in categories if c.name == article_data['category']), categories[0])
            article_tags = [t for t in tags if t.name in article_data['tags']]
            
            article = Article.objects.create(
                title=article_data['title'],
                slug=slugify(article_data['title'], allow_unicode=True),
                author=author,
                category=category,
                excerpt=article_data['excerpt'],
                content=article_data['content'],
                status='published',
                is_featured=article_data.get('is_featured', False),
                published_at=base_date - timedelta(days=i+20),
                views=random.randint(10, 500),
                language='fa'
            )
            
            article.tags.set(article_tags)
            self.stdout.write(f'  ✓ Created: {article.title}')

    def create_book_reviews(self, author, categories):
        """Create 10 test book reviews"""
        books_data = [
            {
                'title': 'Review: "1984" by George Orwell',
                'book_title': '1984',
                'book_author': 'George Orwell',
                'book_year': 1949,
                'rating': 5,
                'excerpt': 'A timeless dystopian masterpiece that remains as relevant today as when it was first published.',
                'content': '<p>George Orwell\'s "1984" is a profound exploration of totalitarianism, surveillance, and the manipulation of truth. The novel follows Winston Smith as he navigates a world where Big Brother watches everything and independent thought is a crime.</p><p>Orwell\'s vision of a dystopian future serves as a powerful warning about the dangers of unchecked government power and the erosion of individual freedoms.</p><p>The novel\'s themes of surveillance, propaganda, and thought control resonate strongly in our modern digital age, making it essential reading for understanding contemporary political dynamics.</p>',
                'category': 'Fiction',
                'is_featured': True
            },
            {
                'title': 'Review: "Sapiens" by Yuval Noah Harari',
                'book_title': 'Sapiens: A Brief History of Humankind',
                'book_author': 'Yuval Noah Harari',
                'book_year': 2011,
                'rating': 5,
                'excerpt': 'A sweeping narrative of human history that challenges our understanding of our species\' journey.',
                'content': '<p>Yuval Noah Harari\'s "Sapiens" offers a compelling overview of human history from the Stone Age to the present. The book explores how Homo sapiens came to dominate the planet through cognitive, agricultural, and scientific revolutions.</p><p>Harari\'s accessible writing style makes complex historical and anthropological concepts understandable to general readers.</p><p>The book raises important questions about the future of our species and the impact of our actions on the planet and other species.</p>',
                'category': 'Non-Fiction',
                'is_featured': True
            },
            {
                'title': 'Review: "The Great Gatsby" by F. Scott Fitzgerald',
                'book_title': 'The Great Gatsby',
                'book_author': 'F. Scott Fitzgerald',
                'book_year': 1925,
                'rating': 5,
                'excerpt': 'A classic American novel that captures the essence of the Jazz Age and the American Dream.',
                'content': '<p>F. Scott Fitzgerald\'s "The Great Gatsby" is a masterful portrayal of 1920s America, exploring themes of wealth, love, and the elusive nature of the American Dream.</p><p>The novel\'s rich symbolism and beautiful prose have made it one of the most celebrated works of American literature.</p><p>Through the tragic story of Jay Gatsby, Fitzgerald examines the moral decay beneath the glittering surface of the Roaring Twenties.</p>',
                'category': 'Fiction',
                'is_featured': False
            },
            {
                'title': 'Review: "Dune" by Frank Herbert',
                'book_title': 'Dune',
                'book_author': 'Frank Herbert',
                'book_year': 1965,
                'rating': 5,
                'excerpt': 'An epic science fiction masterpiece that combines politics, religion, and ecology in a richly imagined universe.',
                'content': '<p>Frank Herbert\'s "Dune" is widely regarded as one of the greatest science fiction novels ever written. Set on the desert planet Arrakis, the novel follows Paul Atreides as he navigates complex political intrigue and mystical forces.</p><p>Herbert creates a fully realized world with intricate systems of politics, religion, and ecology that feel both alien and familiar.</p><p>The novel\'s exploration of themes such as power, prophecy, and environmental stewardship remains relevant and thought-provoking.</p>',
                'category': 'Science Fiction',
                'is_featured': False
            },
            {
                'title': 'Review: "Educated" by Tara Westover',
                'book_title': 'Educated',
                'book_author': 'Tara Westover',
                'book_year': 2018,
                'rating': 5,
                'excerpt': 'A powerful memoir about the transformative power of education and the struggle to find one\'s own path.',
                'content': '<p>Tara Westover\'s "Educated" is a remarkable memoir that chronicles her journey from a survivalist family in rural Idaho to earning a PhD from Cambridge University.</p><p>The book explores themes of family loyalty, education, and the difficult process of breaking away from one\'s upbringing.</p><p>Westover\'s honest and compelling narrative offers insights into the power of education to transform lives and the complexity of family relationships.</p>',
                'category': 'Non-Fiction',
                'is_featured': False
            },
            {
                'title': 'Review: "The Handmaid\'s Tale" by Margaret Atwood',
                'book_title': 'The Handmaid\'s Tale',
                'book_author': 'Margaret Atwood',
                'book_year': 1985,
                'rating': 5,
                'excerpt': 'A chilling dystopian novel that explores themes of women\'s rights, religious extremism, and totalitarian control.',
                'content': '<p>Margaret Atwood\'s "The Handmaid\'s Tale" presents a dystopian future where women\'s rights have been stripped away in a theocratic society called Gilead.</p><p>The novel is narrated by Offred, a handmaid whose sole purpose is to bear children for the ruling class.</p><p>Atwood\'s powerful prose and timely themes make this novel a crucial work for understanding issues of gender, power, and resistance.</p>',
                'category': 'Fiction',
                'is_featured': False
            },
            {
                'title': 'Review: "Sapiens" by Yuval Noah Harari - Part 2',
                'book_title': 'Homo Deus: A Brief History of Tomorrow',
                'book_author': 'Yuval Noah Harari',
                'book_year': 2015,
                'rating': 4,
                'excerpt': 'Harari\'s follow-up explores the future of humanity and the challenges we may face.',
                'content': '<p>In "Homo Deus," Yuval Noah Harari turns his attention to the future, exploring how humanity might evolve in the coming decades and centuries.</p><p>The book examines potential developments in biotechnology, artificial intelligence, and human enhancement.</p><p>Harari raises important questions about what it means to be human and how we should navigate the challenges and opportunities of technological advancement.</p>',
                'category': 'Non-Fiction',
                'is_featured': False
            },
            {
                'title': 'Review: "The Seven Husbands of Evelyn Hugo" by Taylor Jenkins Reid',
                'book_title': 'The Seven Husbands of Evelyn Hugo',
                'book_author': 'Taylor Jenkins Reid',
                'book_year': 2017,
                'rating': 4,
                'excerpt': 'A captivating novel about a reclusive Hollywood icon and the secrets she\'s kept for decades.',
                'content': '<p>Taylor Jenkins Reid\'s novel tells the story of Evelyn Hugo, a legendary Hollywood actress who finally decides to tell her life story to an unknown journalist.</p><p>The book weaves together themes of love, ambition, identity, and the price of fame in a compelling narrative.</p><p>Reid\'s engaging storytelling and well-developed characters make this a page-turner that explores complex relationships and personal growth.</p>',
                'category': 'Fiction',
                'is_featured': False
            },
            {
                'title': 'Review: "The Guns of August" by Barbara Tuchman',
                'book_title': 'The Guns of August',
                'book_author': 'Barbara Tuchman',
                'book_year': 1962,
                'rating': 5,
                'excerpt': 'A masterful historical account of the first month of World War I.',
                'content': '<p>Barbara Tuchman\'s Pulitzer Prize-winning "The Guns of August" provides a detailed and compelling account of the events leading up to and during the first month of World War I.</p><p>Tuchman\'s narrative skill brings historical figures and events to life, making complex diplomatic and military maneuvers understandable.</p><p>The book offers valuable insights into how misunderstandings, miscalculations, and rigid military plans led to one of history\'s greatest conflicts.</p>',
                'category': 'History',
                'is_featured': False
            },
            {
                'title': 'Review: "Project Hail Mary" by Andy Weir',
                'book_title': 'Project Hail Mary',
                'book_author': 'Andy Weir',
                'book_year': 2021,
                'rating': 5,
                'excerpt': 'A thrilling science fiction adventure that combines hard science with humor and heart.',
                'content': '<p>Andy Weir\'s "Project Hail Mary" follows Ryland Grace, a scientist who wakes up alone on a spaceship with no memory of his mission or how he got there.</p><p>The novel combines Weir\'s signature blend of hard science, problem-solving, and humor to create an engaging and entertaining story.</p><p>Through Grace\'s journey, Weir explores themes of cooperation, sacrifice, and the power of scientific thinking to solve seemingly impossible problems.</p>',
                'category': 'Science Fiction',
                'is_featured': False
            },
        ]
        
        base_date = timezone.now()
        for i, book_data in enumerate(books_data):
            category = next((c for c in categories if c.name == book_data['category']), categories[0])
            
            book = BookReview.objects.create(
                title=book_data['title'],
                slug=slugify(book_data['title'], allow_unicode=True),
                author=author,
                category=category,
                book_title=book_data['book_title'],
                book_author=book_data['book_author'],
                book_year=book_data.get('book_year'),
                rating=book_data['rating'],
                excerpt=book_data['excerpt'],
                content=book_data['content'],
                is_published=True,
                is_featured=book_data.get('is_featured', False),
                published_at=base_date - timedelta(days=i*2),
                views=random.randint(20, 800),
                language=book_data.get('language', 'en')
            )
            
            self.stdout.write(f'  ✓ Created: {book.title}')

    def create_persian_book_reviews(self, author, categories):
        """Create Persian book reviews"""
        persian_books_data = [
            {
                'title': 'نقد کتاب «سووشون» - روایتی از خانواده‌ای درگیر تاریخ',
                'book_title': 'سووشون',
                'book_author': 'سیمین دانشور',
                'book_year': 1969,
                'rating': 5,
                'excerpt': 'رمانی ماندگار درباره زیست ایرانیان در سال‌های پرتلاطم دهه ۲۰ شمسی.',
                'content': '<p>«سووشون» روایتی صمیمی و در عین حال سیاسی از خانواده‌ای در شیراز است که در میانه آشوب جنگ جهانی دوم قرار می‌گیرد.</p><p>سیمین دانشور با خلق شخصیت‌های ماندگار، تضاد سنت و مدرنیته و مقاومت زنان ایرانی را به زیبایی نشان می‌دهد.</p><p>این رمان نه تنها تصویری از تاریخ معاصر ارائه می‌کند بلکه به پرسش‌های اخلاقی و اجتماعی آن دوران نیز می‌پردازد.</p>',
                'category': 'Fiction'
            },
            {
                'title': 'معرفی «کلیدر» و حماسه روستایی محمود دولت‌آبادی',
                'book_title': 'کلیدر',
                'book_author': 'محمود دولت‌آبادی',
                'rating': 5,
                'excerpt': 'حماسه‌ای چندجلدی درباره عشق، مقاومت و زیست روستایی خراسان.',
                'content': '<p>«کلیدر» با نثری شاعرانه و پرجزئیات، سرگذشت گل‌محمد و طایفه‌اش را روایت می‌کند که در برابر ظلم و بی‌عدالتی می‌ایستند.</p><p>دولت‌آبادی در این اثر به ظرافت روابط انسانی، نقش زنان و پیوند ناگسستنی مردم با زمین را به تصویر می‌کشد.</p><p>خواندن این رمان تجربه‌ای نفس‌گیر است که تاریخ شفاهی و فرهنگ محلی را زنده نگه می‌دارد.</p>',
                'category': 'Fiction'
            },
            {
                'title': 'مروری بر «چراغ‌ها را من خاموش می‌کنم»',
                'book_title': 'چراغ‌ها را من خاموش می‌کنم',
                'book_author': 'زویا پیرزاد',
                'rating': 4,
                'excerpt': 'روایتی از روزمرگی، سکوت و آرزوهای پنهان زنان ارمنی آبادان.',
                'content': '<p>پیرزاد با نثر دقیق و سرشار از جزئیات، زندگی زنی خانه‌دار را روایت می‌کند که میان مسئولیت‌های خانوادگی و خواسته‌های شخصی‌اش در نوسان است.</p><p>فضاسازی آبادان دهه ۴۰ و روابط انسانی ظریف، این رمان را به اثری متمایز در ادبیات معاصر ایران تبدیل کرده است.</p><p>کتاب به مخاطب یادآوری می‌کند که تغییرات بزرگ از دل گفت‌وگوهای کوچک و صبر شکل می‌گیرند.</p>',
                'category': 'Fiction'
            },
            {
                'title': 'گزارشی از کتاب «دا»؛ روایت صریح از جنگ',
                'book_title': 'دا',
                'book_author': 'زهرا حسینی با تدوین سیده اعظم حسینی',
                'rating': 5,
                'excerpt': 'خاطراتی مستند از روزهای آغازین دفاع مقدس در خرمشهر.',
                'content': '<p>کتاب «دا» با زبانی ساده اما تکان‌دهنده، روایت زندگی دختر جوانی است که با آغاز جنگ، نقش‌های تازه‌ای را تجربه می‌کند.</p><p>این خاطرات، تصویر زنانی را نشان می‌دهد که دوشادوش مردان در خط مقدم، امداد، پشتیبانی و مقاومت می‌کنند.</p><p>اهمیت کتاب در مستند بودن، جزئیات دقیق و نگاه انسانی آن به جنگ است.</p>',
                'category': 'History'
            },
            {
                'title': 'نقد کتاب «من او»؛ پیوند عرفان و داستان',
                'book_title': 'من او',
                'book_author': 'رضا امیرخانی',
                'rating': 4,
                'excerpt': 'رمانی معاصر که عشق زمینی و مفاهیم معنوی را در کنار هم پیش می‌برد.',
                'content': '<p>«من او» داستان علی فتاح و عشق تمام‌عیارش را روایت می‌کند که در دل تاریخ و تحولات تهران قدیم رخ می‌دهد.</p><p>امیرخانی با نثری ترکیب‌یافته از سنت و نوگرایی، مفاهیم عرفانی را با دغدغه‌های اجتماعی پیوند می‌زند.</p><p>رمان مخاطب را به کشف هویت، ایمان و مسئولیت فردی فرا می‌خواند.</p>',
                'category': 'Fiction'
            },
            {
                'title': 'مروری بر کتاب «تنها گریه کن»',
                'book_title': 'تنها گریه کن',
                'book_author': 'معصومه آباد',
                'rating': 4,
                'excerpt': 'خاطرات آزادگان زن ایرانی و تجربه اسارت در زندان‌های عراق.',
                'content': '<p>کتاب «تنها گریه کن» روایت صریح و پر از امیدی است از روزهای اسارت و بازجویی که با تکیه بر ایمان و همبستگی زنان سپری می‌شود.</p><p>نویسنده جزئیات زیست روزمره، نامه‌ها و لحظات شکننده را به شکلی روایت می‌کند که مخاطب پیوندی عاطفی با شخصیت‌ها برقرار می‌کند.</p><p>این اثر بخشی مغفول از تاریخ شفاهی جنگ را زنده کرده و اهمیت اشتراک تجربه‌های زنانه را برجسته می‌کند.</p>',
                'category': 'Non-Fiction'
            },
        ]
        
        base_date = timezone.now()
        for i, book_data in enumerate(persian_books_data):
            category = next((c for c in categories if c.name == book_data['category']), categories[0])
            
            book = BookReview.objects.create(
                title=book_data['title'],
                slug=slugify(book_data['title'], allow_unicode=True),
                author=author,
                category=category,
                book_title=book_data['book_title'],
                book_author=book_data['book_author'],
                book_year=book_data.get('book_year'),
                rating=book_data['rating'],
                excerpt=book_data['excerpt'],
                content=book_data['content'],
                is_published=True,
                is_featured=book_data.get('is_featured', False),
                published_at=base_date - timedelta(days=40 + i*3),
                views=random.randint(50, 900),
                language='fa'
            )
            
            self.stdout.write(f'  ✓ Created (FA): {book.title}')

    def create_movie_reviews(self, author, categories):
        """Create 15 test movie reviews"""
        movies_data = [
            {
                'title': 'Review: "The Shawshank Redemption"',
                'movie_title': 'The Shawshank Redemption',
                'director': 'Frank Darabont',
                'year': 1994,
                'genre': 'Drama',
                'rating': 5,
                'excerpt': 'A powerful story of hope, friendship, and redemption set in a maximum-security prison.',
                'content': '<p>"The Shawshank Redemption" is widely considered one of the greatest films ever made. Based on a Stephen King novella, the film tells the story of Andy Dufresne, a banker wrongly convicted of murder.</p><p>Through Andy\'s friendship with fellow inmate Red, the film explores themes of hope, perseverance, and the human spirit\'s ability to endure even in the darkest circumstances.</p><p>Tim Robbins and Morgan Freeman deliver outstanding performances, and the film\'s message of hope and redemption resonates deeply with audiences.</p>',
                'category': 'Drama',
                'is_featured': True
            },
            {
                'title': 'Review: "Inception"',
                'movie_title': 'Inception',
                'director': 'Christopher Nolan',
                'year': 2010,
                'genre': 'Thriller',
                'rating': 5,
                'excerpt': 'A mind-bending thriller that explores the boundaries of reality and dreams.',
                'content': '<p>Christopher Nolan\'s "Inception" is a masterful blend of science fiction, action, and psychological thriller. The film follows Dom Cobb, a skilled thief who specializes in entering people\'s dreams to steal secrets.</p><p>The film\'s complex narrative structure and stunning visual effects create an immersive experience that challenges viewers to question the nature of reality.</p><p>Nolan\'s direction, combined with Hans Zimmer\'s iconic score, creates a cinematic experience that is both intellectually stimulating and emotionally engaging.</p>',
                'category': 'Thriller',
                'is_featured': True
            },
            {
                'title': 'Review: "Parasite"',
                'movie_title': 'Parasite',
                'director': 'Bong Joon-ho',
                'year': 2019,
                'genre': 'Thriller',
                'rating': 5,
                'excerpt': 'A darkly comedic thriller that brilliantly explores class inequality and social dynamics.',
                'content': '<p>Bong Joon-ho\'s "Parasite" made history as the first non-English language film to win the Academy Award for Best Picture. The film tells the story of the Kim family, who scheme to become employed by the wealthy Park family.</p><p>The film masterfully blends genres, shifting from comedy to thriller to horror while maintaining a sharp social commentary on class inequality.</p><p>Bong\'s direction is precise and powerful, using visual storytelling to enhance the film\'s themes and create a truly memorable cinematic experience.</p>',
                'category': 'Thriller',
                'is_featured': True
            },
            {
                'title': 'Review: "The Dark Knight"',
                'movie_title': 'The Dark Knight',
                'director': 'Christopher Nolan',
                'year': 2008,
                'genre': 'Action',
                'rating': 5,
                'excerpt': 'A superhero film that transcends its genre to become a complex exploration of morality and chaos.',
                'content': '<p>Christopher Nolan\'s "The Dark Knight" is widely regarded as one of the greatest superhero films ever made. The film pits Batman against the Joker in a battle that tests the limits of heroism and morality.</p><p>Heath Ledger\'s iconic performance as the Joker earned him a posthumous Academy Award and remains one of the most memorable villain portrayals in cinema history.</p><p>The film\'s exploration of themes such as order versus chaos, the nature of heroism, and the cost of fighting evil makes it a thought-provoking work that elevates the superhero genre.</p>',
                'category': 'Action',
                'is_featured': False
            },
            {
                'title': 'Review: "Pulp Fiction"',
                'movie_title': 'Pulp Fiction',
                'director': 'Quentin Tarantino',
                'year': 1994,
                'genre': 'Thriller',
                'rating': 5,
                'excerpt': 'A groundbreaking film that revolutionized independent cinema with its non-linear narrative and sharp dialogue.',
                'content': '<p>Quentin Tarantino\'s "Pulp Fiction" is a landmark film that redefined independent cinema in the 1990s. The film weaves together multiple interconnected stories involving criminals, hitmen, and various colorful characters.</p><p>Tarantino\'s signature style—sharp dialogue, pop culture references, and non-linear storytelling—is on full display, creating an engaging and entertaining experience.</p><p>The film\'s impact on cinema cannot be overstated, influencing countless filmmakers and establishing Tarantino as one of the most distinctive voices in modern cinema.</p>',
                'category': 'Thriller',
                'is_featured': False
            },
            {
                'title': 'Review: "The Grand Budapest Hotel"',
                'movie_title': 'The Grand Budapest Hotel',
                'director': 'Wes Anderson',
                'year': 2014,
                'genre': 'Comedy',
                'rating': 5,
                'excerpt': 'A visually stunning and whimsically charming film that showcases Wes Anderson\'s unique directorial style.',
                'content': '<p>Wes Anderson\'s "The Grand Budapest Hotel" is a delightful comedy-drama that tells the story of a legendary concierge and his lobby boy at a famous European hotel between the wars.</p><p>Anderson\'s meticulous attention to detail, symmetrical compositions, and pastel color palette create a visually stunning and distinctive aesthetic.</p><p>The film\'s ensemble cast, including Ralph Fiennes, delivers excellent performances, and the story balances humor, adventure, and melancholy in Anderson\'s signature style.</p>',
                'category': 'Comedy',
                'is_featured': False
            },
            {
                'title': 'Review: "Interstellar"',
                'movie_title': 'Interstellar',
                'director': 'Christopher Nolan',
                'year': 2014,
                'genre': 'Drama',
                'rating': 5,
                'excerpt': 'An epic science fiction film that explores love, time, and humanity\'s place in the universe.',
                'content': '<p>Christopher Nolan\'s "Interstellar" is a visually spectacular science fiction epic that follows a team of explorers traveling through a wormhole in search of a new home for humanity.</p><p>The film combines hard science with emotional storytelling, exploring themes of love, sacrifice, and the human drive to explore and survive.</p><p>Hans Zimmer\'s powerful score and stunning visual effects create an immersive experience that captures the vastness and wonder of space exploration.</p>',
                'category': 'Drama',
                'is_featured': False
            },
            {
                'title': 'Review: "Get Out"',
                'movie_title': 'Get Out',
                'director': 'Jordan Peele',
                'year': 2017,
                'genre': 'Thriller',
                'rating': 5,
                'excerpt': 'A brilliant horror-thriller that uses genre conventions to explore racism and social commentary.',
                'content': '<p>Jordan Peele\'s directorial debut "Get Out" is a masterful blend of horror, thriller, and social commentary. The film follows a young African American man who visits his white girlfriend\'s family estate.</p><p>Peele uses horror tropes to explore deeper themes of racism, cultural appropriation, and the insidious nature of modern prejudice.</p><p>The film\'s clever writing, strong performances, and effective use of suspense make it both entertaining and thought-provoking, establishing Peele as a major new voice in cinema.</p>',
                'category': 'Thriller',
                'is_featured': False
            },
            {
                'title': 'Review: "Mad Max: Fury Road"',
                'movie_title': 'Mad Max: Fury Road',
                'director': 'George Miller',
                'year': 2015,
                'genre': 'Action',
                'rating': 5,
                'excerpt': 'A high-octane action masterpiece that redefines the post-apocalyptic genre.',
                'content': '<p>George Miller\'s "Mad Max: Fury Road" is a relentless, high-energy action film that takes place in a post-apocalyptic wasteland. The film follows Max and Furiosa as they attempt to escape a tyrannical warlord.</p><p>The film\'s practical effects, stunning cinematography, and non-stop action sequences create an exhilarating cinematic experience.</p><p>Charlize Theron\'s performance as Furiosa is particularly strong, and the film\'s feminist themes add depth to the action-packed narrative.</p>',
                'category': 'Action',
                'is_featured': False
            },
            {
                'title': 'Review: "The Social Network"',
                'movie_title': 'The Social Network',
                'director': 'David Fincher',
                'year': 2010,
                'genre': 'Drama',
                'rating': 5,
                'excerpt': 'A compelling drama about the creation of Facebook and the complexities of friendship and ambition.',
                'content': '<p>David Fincher\'s "The Social Network" tells the story of Mark Zuckerberg and the creation of Facebook. Aaron Sorkin\'s sharp screenplay and Fincher\'s precise direction create a compelling narrative.</p><p>The film explores themes of ambition, friendship, betrayal, and the rapid pace of technological innovation in the digital age.</p><p>Jesse Eisenberg delivers a strong performance as Zuckerberg, and the film\'s examination of the social and personal costs of success resonates deeply.</p>',
                'category': 'Drama',
                'is_featured': False
            },
            {
                'title': 'Review: "Whiplash"',
                'movie_title': 'Whiplash',
                'director': 'Damien Chazelle',
                'year': 2014,
                'genre': 'Drama',
                'rating': 5,
                'excerpt': 'An intense drama about the pursuit of perfection and the price of greatness.',
                'content': '<p>Damien Chazelle\'s "Whiplash" is a gripping drama about a young jazz drummer and his demanding instructor. The film explores the relationship between mentor and student, and the extreme measures some take in pursuit of artistic excellence.</p><p>J.K. Simmons\' Oscar-winning performance as the ruthless instructor is unforgettable, and Miles Teller\'s portrayal of the driven student is equally compelling.</p><p>The film\'s intense pacing, powerful performances, and thought-provoking themes about ambition and sacrifice make it a standout work.</p>',
                'category': 'Drama',
                'is_featured': False
            },
            {
                'title': 'Review: "The Matrix"',
                'movie_title': 'The Matrix',
                'director': 'The Wachowskis',
                'year': 1999,
                'genre': 'Action',
                'rating': 5,
                'excerpt': 'A groundbreaking science fiction film that revolutionized action cinema and explored philosophical themes.',
                'content': '<p>The Wachowskis\' "The Matrix" is a landmark film that combined groundbreaking visual effects with deep philosophical themes. The film follows Neo as he discovers that reality is a computer simulation.</p><p>The film\'s innovative "bullet time" effects and martial arts sequences revolutionized action cinema, while its exploration of themes such as reality, choice, and free will added intellectual depth.</p><p>"The Matrix" remains influential, inspiring countless films and discussions about the nature of reality and technology\'s role in our lives.</p>',
                'category': 'Action',
                'is_featured': False
            },
            {
                'title': 'Review: "Her"',
                'movie_title': 'Her',
                'director': 'Spike Jonze',
                'year': 2013,
                'genre': 'Drama',
                'rating': 5,
                'excerpt': 'A thoughtful and emotional exploration of love, connection, and technology in the modern world.',
                'content': '<p>Spike Jonze\'s "Her" tells the story of a man who develops a relationship with an artificial intelligence operating system. The film explores themes of loneliness, connection, and what it means to love in the digital age.</p><p>Joaquin Phoenix delivers a nuanced performance, and Scarlett Johansson\'s voice work as the AI is remarkably expressive and engaging.</p><p>The film\'s thoughtful exploration of human relationships and technology raises important questions about connection, intimacy, and the future of human-AI interaction.</p>',
                'category': 'Drama',
                'is_featured': False
            },
            {
                'title': 'Review: "The Big Short"',
                'movie_title': 'The Big Short',
                'director': 'Adam McKay',
                'year': 2015,
                'genre': 'Drama',
                'rating': 5,
                'excerpt': 'A smart and entertaining film that explains the 2008 financial crisis through compelling storytelling.',
                'content': '<p>Adam McKay\'s "The Big Short" uses creative storytelling techniques to explain the complex financial instruments and events that led to the 2008 financial crisis.</p><p>The film follows several groups of investors who predicted the housing market collapse and bet against it. McKay uses humor, celebrity cameos, and direct-to-camera explanations to make complex financial concepts accessible.</p><p>The film\'s strong ensemble cast and engaging narrative make it both entertaining and educational, offering insights into the financial system and its vulnerabilities.</p>',
                'category': 'Drama',
                'is_featured': False
            },
            {
                'title': 'Review: "Everything Everywhere All at Once"',
                'movie_title': 'Everything Everywhere All at Once',
                'director': 'Daniel Kwan, Daniel Scheinert',
                'year': 2022,
                'genre': 'Comedy',
                'rating': 5,
                'excerpt': 'A wildly creative and emotionally resonant film that defies genre conventions.',
                'content': '<p>"Everything Everywhere All at Once" is a genre-defying film that combines science fiction, action, comedy, and family drama. The film follows Evelyn Wang as she discovers she can access parallel universes.</p><p>The film\'s creative visual style, emotional depth, and exploration of themes such as family, identity, and the meaning of life make it a truly unique cinematic experience.</p><p>Michelle Yeoh\'s performance earned her an Academy Award, and the film\'s blend of absurd humor and genuine emotion creates a memorable and moving experience.</p>',
                'category': 'Comedy',
                'is_featured': False
            },
        ]
        
        base_date = timezone.now()
        for i, movie_data in enumerate(movies_data):
            category = next((c for c in categories if c.name == movie_data['category']), categories[0])
            
            movie = MovieReview.objects.create(
                title=movie_data['title'],
                slug=slugify(movie_data['title'], allow_unicode=True),
                author=author,
                category=category,
                movie_title=movie_data['movie_title'],
                director=movie_data['director'],
                year=movie_data.get('year'),
                genre=movie_data.get('genre', ''),
                rating=movie_data['rating'],
                excerpt=movie_data['excerpt'],
                content=movie_data['content'],
                is_published=True,
                is_featured=movie_data.get('is_featured', False),
                published_at=base_date - timedelta(days=i*2),
                views=random.randint(30, 1000),
                language=movie_data.get('language', 'en')
            )
            
            self.stdout.write(f'  ✓ Created: {movie.title}')

    def create_persian_movie_reviews(self, author, categories):
        """Create Persian movie reviews"""
        persian_movies_data = [
            {
                'title': 'نقد فیلم «جدایی نادر از سیمین»',
                'movie_title': 'جدایی نادر از سیمین',
                'director': 'اصغر فرهادی',
                'year': 2011,
                'genre': 'درام خانوادگی',
                'rating': 5,
                'excerpt': 'روایتی ظریف از فروپاشی یک خانواده و تنش‌های اجتماعی پنهان.',
                'content': '<p>فرهادی با بهره‌گیری از دوربین سیال و دیالوگ‌های دقیق، گره‌های اخلاقی زندگی طبقه متوسط را به تصویر می‌کشد.</p><p>بازی‌های درخشان پیمان معادی و لیلا حاتمی، به همراه ریتم پرتعلیق، تماشاگر را تا لحظه آخر درگیر نگه می‌دارد.</p><p>فیلم نشان می‌دهد چگونه انتخاب‌های کوچک، پیامدهای بزرگ اجتماعی و عاطفی به دنبال دارند.</p>',
                'category': 'Drama'
            },
            {
                'title': 'بررسی فیلم «درباره الی»',
                'movie_title': 'درباره الی',
                'director': 'اصغر فرهادی',
                'year': 2009,
                'genre': 'درام معمایی',
                'rating': 5,
                'excerpt': 'سفر دوستانه‌ای که به تدریج بدل به بحرانی اخلاقی و روانی می‌شود.',
                'content': '<p>فیلم با خلق فضایی سرشار از ناگفته‌ها، روابط ظریف میان دوستان قدیمی را کالبدشکافی می‌کند.</p><p>رخداد ناپدید شدن، پرده از لایه‌های پنهان شخصیت‌ها برمی‌دارد و مفهوم مسئولیت جمعی را زیر سؤال می‌برد.</p><p>تدوین دقیق و بازی گروهی هماهنگ، «درباره الی» را به یکی از مهم‌ترین آثار معاصر ایران بدل کرده است.</p>',
                'category': 'Thriller'
            },
            {
                'title': 'نقد فیلم «متری شیش و نیم»',
                'movie_title': 'متری شیش و نیم',
                'director': 'سعید روستایی',
                'year': 2019,
                'genre': 'درام پلیسی',
                'rating': 4,
                'excerpt': 'نگاهی واقع‌گرایانه به چرخه اعتیاد و شبکه قاچاق در پایتخت.',
                'content': '<p>روستایی با استفاده از لانگ‌شات‌های مستندگونه، نبض تند شهر و پیچیدگی پرونده‌های پلیسی را به تصویر می‌کشد.</p><p>نمایش همزمان تلاش پلیس و سرنوشت مصرف‌کنندگان، پرسشی جدی درباره ریشه‌های اجتماعی اعتیاد طرح می‌کند.</p><p>فیلم به مدد بازی نوید محمدزاده و پیمان معادی، تعلیقی انسانی و باورپذیر خلق می‌کند.</p>',
                'category': 'Action'
            },
            {
                'title': 'تحلیل فیلم «طعم گیلاس»',
                'movie_title': 'طعم گیلاس',
                'director': 'عباس کیارستمی',
                'year': 1997,
                'genre': 'درام فلسفی',
                'rating': 5,
                'excerpt': 'سفری مینیمالیستی درباره معنای زندگی، مرگ و انتخاب فردی.',
                'content': '<p>کیارستمی با روایت جاده‌ای و ریتم تامل‌برانگیز، مخاطب را در کنار شخصیت اصلی قرار می‌دهد تا به پرسش‌های بنیادین بیندیشد.</p><p>استفاده از لوکیشن‌های بیابانی و سکوت‌های طولانی، حس تعلیق و درون‌نگری را دوچندان می‌کند.</p><p>پایان‌بندی متا و بازتابی فیلم، تجربه دیداری منحصربه‌فردی برای مخاطب می‌سازد.</p>',
                'category': 'Drama'
            },
            {
                'title': 'نگاهی به فیلم «ابد و یک روز»',
                'movie_title': 'ابد و یک روز',
                'director': 'سعید روستایی',
                'year': 2016,
                'genre': 'درام اجتماعی',
                'rating': 5,
                'excerpt': 'پرتره‌ای گزنده از خانواده‌ای کارگری در حاشیه شهر.',
                'content': '<p>فیلم با بهره‌گیری از بازی‌های بی‌نظیر پریناز ایزدیار و پیمان معادی، درماندگی و آرزوهای سرکوب‌شده اعضای خانواده را نشان می‌دهد.</p><p>نویسندگی تیزبینانه روستایی، تضاد نسل‌ها و بحران اقتصادی را بدون شعارزدگی مطرح می‌کند.</p><p>«ابد و یک روز» نمونه‌ای شاخص از رئالیسم اجتماعی در سینمای ایران است.</p>',
                'category': 'Drama'
            },
            {
                'title': 'فیلم «قهرمان»؛ کشمکش اخلاق و رسانه',
                'movie_title': 'قهرمان',
                'director': 'اصغر فرهادی',
                'year': 2021,
                'genre': 'درام',
                'rating': 4,
                'excerpt': 'روایت مردی که درگیر بازی رسانه‌ای و داوری افکار عمومی می‌شود.',
                'content': '<p>فرهادی در «قهرمان» نشان می‌دهد چگونه حقیقت در عصر شبکه‌های اجتماعی به سرعت دستکاری می‌شود.</p><p>شخصیت رحیم با بازی امیر جدیدی، میان امید به رهایی و بار گذشته گرفتار است.</p><p>فیلم با ریتمی آرام اما پرتنش، ارزش صداقت و پیامد شایعات را یادآوری می‌کند.</p>',
                'category': 'Drama'
            },
        ]
        
        base_date = timezone.now()
        for i, movie_data in enumerate(persian_movies_data):
            category = next((c for c in categories if c.name == movie_data['category']), categories[0])
            
            movie = MovieReview.objects.create(
                title=movie_data['title'],
                slug=slugify(movie_data['title'], allow_unicode=True),
                author=author,
                category=category,
                movie_title=movie_data['movie_title'],
                director=movie_data['director'],
                year=movie_data.get('year'),
                genre=movie_data.get('genre', ''),
                rating=movie_data['rating'],
                excerpt=movie_data['excerpt'],
                content=movie_data['content'],
                is_published=True,
                is_featured=movie_data.get('is_featured', False),
                published_at=base_date - timedelta(days=80 + i*3),
                views=random.randint(60, 1600),
                language='fa'
            )
            
            self.stdout.write(f'  ✓ Created (FA): {movie.title}')

