from django.utils import timezone

from datetime import datetime
from pytz import timezone as tz

from event_manager.settings import TIME_ZONE
from main.models import EVENT_STATUSES, User

superuser = User.objects.get(username='admin')

event_01 = {
    'title': "JetBrains .NET Days Online 2021",
    'description': "JetBrains .NET Days Online are a free virtual event "
                   "where community speakers cover topics they are passionate about, "
                   "ranging from deep technical .NET content and speakers’ "
                   "experiences with specific tools and technologies, to personal development."
                   "Submit a talk and share your experience! We welcome all topics "
                   "that would be relevant to the wider .NET community. "
                   "We'd appreciate some link to a JetBrains product "
                   "(not necessarily product focused, maybe just use it for demos).",
    'location': "Online",
    'website': "https://pages.jetbrains.com/dotnet-days-2021/blog",
    'author': superuser,
    'status': EVENT_STATUSES.WAITING,
    'start_date': timezone.make_aware(datetime.strptime("11/05/21 00:00", "%d/%m/%y %H:%M"), tz(TIME_ZONE)),
    'end_date': timezone.make_aware(datetime.strptime("12/05/21 23:59", "%d/%m/%y %H:%M"), tz(TIME_ZONE)),
}

event_02 = {
    'title': "PyCom US 2021",
    'description': "First and foremost we want to send our very best to you "
                   "as well as your family and friends as we all continue to navigate the challenges of COVID-19. "
                   "With the safety of our community in mind the decision was made to hold the event virtually. "
                   "You can read the announcement details here. Our staff and volunteers have been working "
                   "to bring you an event that will be full of great content, plenty of networking, "
                   "dedicated time with sponsors, 5K runs, social events and so much more! "
                   "As we work to finalize our plans, we will keep you informed "
                   "with updates on the exciting developments taking place.",
    'location': "Online",
    'website': "https://us.pycon.org/2021/",
    'author': superuser,
    'status': EVENT_STATUSES.WAITING,
    'start_date': timezone.make_aware(datetime.strptime("12/05/21 18:00", "%d/%m/%y %H:%M"), tz(TIME_ZONE)),
    'end_date': timezone.make_aware(datetime.strptime("18/05/21 23:59", "%d/%m/%y %H:%M"), tz(TIME_ZONE)),
}

event_03 = {
    'title': "DevOps Pro Europe 2021",
    'description': "Annual DevOps Pro Europe conference covers the core principles "
                   "and concepts of the DevOps methodology and demonstrates "
                   "how to use the most common DevOps patterns to develop, "
                   "deploy and maintain applications on-premises and in the cloud. "
                   "DevOps Pro Europe conference puts the spotlight on "
                   "entire software delivery pipeline.",
    'location': "Vilnius, Online",
    'website': "https://devopspro.lt/",
    'author': superuser,
    'status': EVENT_STATUSES.WAITING,
    'start_date': timezone.make_aware(datetime.strptime("11/05/21 09:00", "%d/%m/%y %H:%M"), tz(TIME_ZONE)),
    'end_date': timezone.make_aware(datetime.strptime("13/05/21 16:10", "%d/%m/%y %H:%M"), tz(TIME_ZONE)),
}

event_04 = {
    'title': "AGILE100",
    'description': "Our Agile100 virtual conference series aims to bring the knowledge "
                   "and experience of the world’s top 100 agile thinkers and "
                   "speakers to everyone across the globe. "
                   "We want to embrace the latest technology to help spread the best ideas. "
                   "At our core, we believe that people with access to knowledge and "
                   "information can tackle any challenge and make our world more productive, "
                   "more humane, and more sustainable.",
    'location': "Online",
    'website': "https://partner.agile-academy.com/en/agile100/",
    'author': superuser,
    'status': EVENT_STATUSES.WAITING,
    'start_date': timezone.make_aware(datetime.strptime("14/05/21 14:50", "%d/%m/%y %H:%M"), tz(TIME_ZONE)),
    'end_date': timezone.make_aware(datetime.strptime("14/05/21 19:30", "%d/%m/%y %H:%M"), tz(TIME_ZONE)),
}

event_05 = {
    'title': "GlueCon 2021",
    'description': "GlueCon is a developer-oriented conference focused "
                   "on providing the latest in-depth technical information, "
                   "presented in a format that fosters community. "
                   "GlueCon’s topics change from year to year, but include things like APIs, "
                   "DevOps, Serverless, Edge Computing, Containers, Microservices, "
                   "Blockchain-driven applications, and the newest tools "
                   "and platforms driving technology. If you’re tired of sales pitches "
                   "disguised as talks, sessions that never do more than scratch the surface, "
                   "throngs of people that seem more concerned with the after-parties than the education, "
                   "and networking that has no lasting impact, then GlueCon is for you. "
                   "Hand-crafted by the husband and wife team of Kim and Eric Norlin, "
                   "GlueCon is entering its 11th year of existence. During that time, huge numbers of protocols, "
                   "projects, technologies and startups have launched at GlueCon. "
                   "Quite simply, GlueCon is where a welcoming community of experts gather annually "
                   "to learn about what’s next - years before those topics will appear at other conferences.Join us!",
    'location': "Broomfield, Colorado",
    'website': "https://www.gluecon.com/",
    'author': superuser,
    'status': EVENT_STATUSES.WAITING,
    'start_date': timezone.make_aware(datetime.strptime("17/11/21 00:00", "%d/%m/%y %H:%M"), tz(TIME_ZONE)),
    'end_date': timezone.make_aware(datetime.strptime("18/11/21 23:59", "%d/%m/%y %H:%M"), tz(TIME_ZONE)),
}

event_06 = {
    'title': "Blockchain Economy 2021",
    'description': "The second of the most comprehensive Blockchain and cryptocurrency conference in MENA "
                   "and Eurasia will take place during two days in Istanbul on February 20-21, "
                   "2020 with the best international names in the sector. The conference will be the largest meeting "
                   "in the region on behalf of the world of blockchain and cryptocurrency, with a wide range of topics "
                   "focused on the financial technologies of the future, extensive networking opportunities and "
                   "participation from more than 60 countries. "
                   "Turkey is a significant country for the world cryptocurrency community, "
                   "thus this region preserves being an attractive meeting center for other countries. "
                   "Indeed, according to Statista Global Consumer Survey 2019, Turkey is ranked first in "
                   "the world cryptocurrency ownership. "
                   "Currently 20% of the population in Turkey owns cryptocurrency. The main topics of the "
                   "Blockchain Economy 2020 conference "
                   "will include Blockchain technology and cryptocurrency, as well as "
                   "Artificial Intelligence, Big Data, "
                   "Decentralized Technologies, IoT and Global Citizenship.",
    'location': "Istanbul, Turkey",
    'website': "https://www.blockchaineconomy.istanbul/",
    'author': superuser,
    'status': EVENT_STATUSES.WAITING,
    'start_date': timezone.make_aware(datetime.strptime("22/11/21 00:00", "%d/%m/%y %H:%M"), tz(TIME_ZONE)),
    'end_date': timezone.make_aware(datetime.strptime("22/11/21 23:59", "%d/%m/%y %H:%M"), tz(TIME_ZONE)),
}

events = [event_01, event_02, event_03, event_04, event_05, event_06]
