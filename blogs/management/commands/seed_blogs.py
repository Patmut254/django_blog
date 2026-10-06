from datetime import timedelta

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone

from assignments.models import About
from blogs.models import Blog, Category

UNSPLASH = 'https://images.unsplash.com/photo-{}?w=1600&q=80&auto=format&fit=crop'

# (category, title, unsplash photo id, featured, short description, body)
POSTS = [
    ('Sports Today', 'The Science Behind the Perfect Free Kick', '1574629810360-7efbbe195018', True,
     'Spin, speed and a wall of defenders: why the best free-kick takers spend years mastering a strike that lasts less than a second.',
     """A well-struck free kick looks like art, but it is really applied physics. When a player strikes the ball off-centre, it leaves the boot spinning, and that spin drags a thin layer of air around with it. Pressure drops on one side of the ball and rises on the other, bending its path in what scientists call the Magnus effect.

The very best takers combine that curl with dip. By striking through the lower half of the ball with the laces and a short follow-through, they add topspin that pulls the ball down sharply once it clears the wall. Goalkeepers read the first half of the flight and are beaten by the second.

Then there is the knuckleball, the strike that barely spins at all. Without spin, the air flowing around the ball becomes unstable, and tiny changes in the seams cause it to wobble unpredictably. Even the player who hits it cannot be sure where it will finish, which is exactly why goalkeepers fear it.

None of this happens by accident. Specialist coaches say elite takers practise hundreds of repetitions a week, often from the same five or six positions around the box. They learn how a wet ball skids, how a light ball floats at altitude and how much a crowd's noise changes their run-up rhythm.

The result is a moment that looks spontaneous but is built on thousands of hours of quiet, repetitive work on empty training pitches."""),

    ('Sports Today', 'Inside the Mind of an Elite Marathon Runner', '1552674605-db6ffd4facb5', True,
     'For the world\'s best distance runners, the hardest part of 42.195 kilometres is not the legs. It is the conversation inside their heads.',
     """By the thirty-kilometre mark of a marathon, almost every runner's body is sending the same message: stop. Glycogen stores are nearly empty, muscle fibres are damaged and core temperature is climbing. What separates the elite from everyone else is not the absence of that message but how they respond to it.

Sports psychologists describe two broad strategies. Association means paying close attention to the body: breathing, cadence, the feel of each foot strike. Dissociation means drifting away from discomfort by thinking about something else entirely. Research suggests the fastest runners lean heavily on association, constantly checking in with their bodies and adjusting pace in tiny increments.

Many elite athletes also break the race into small, manageable pieces. Instead of thinking about the twelve kilometres still to go, they focus on reaching the next drinks station or the next turn in the road. Each small target is a win, and each win buys a little more resolve.

Training builds this mental muscle as much as it builds physical fitness. Long runs at goal pace teach athletes what controlled discomfort feels like, so that on race day the feeling is familiar rather than frightening.

For recreational runners, the lesson is simple: the mind can be trained just like the legs. Practise staying present on hard sessions, and the final kilometres of your next race may feel a little less lonely."""),

    ('Sports Today', 'Why the Three-Point Revolution Is Here to Stay', '1546519638-68e109498ffc', False,
     'Basketball has been transformed by a simple bit of maths. Here is why teams keep shooting from deep, and what it has done to the game.',
     """For decades, basketball coaches preached the value of getting close to the basket. Then analysts did some arithmetic. A team that makes 36 percent of its three-point attempts scores about 1.08 points per shot. A team that makes 45 percent of its long two-pointers scores just 0.9. The gap may look small, but over a season of thousands of possessions it decides championships.

That insight reshaped the sport. Teams now prize players who can space the floor, and the mid-range jumper, once the signature shot of the game's greatest scorers, has become comparatively rare. Offences are designed to produce either a layup or an open three, with very little in between.

Critics argue that the style has made games feel repetitive, with long stretches of players hoisting shots from well beyond the arc. Supporters counter that it has opened the floor, made the game faster and rewarded skill over size.

The change has reached every level. Youth coaches report that young players now spend more time practising long-range shooting than post moves, and that skill development has become more position-less as a result.

Whether you love it or not, the maths has not changed, and as long as three is greater than two, the long ball is not going anywhere."""),

    ('Sports Today', 'How Swimmers Shave Hundredths of a Second', '1530549387789-4c1017266635', False,
     'At the elite level, races are decided by margins smaller than a blink. Swimmers chase those margins in the details most spectators never notice.',
     """In elite swimming, a hundredth of a second can separate a gold medal from fourth place. That is roughly the length of a fingernail at race speed. To find those margins, swimmers and coaches obsess over parts of the race that casual viewers barely see.

The start is the first battleground. Modern starting blocks have an angled back plate that lets swimmers push off with both legs, and the best athletes spend hours refining their reaction time and entry angle so that they slip into the water through a single small hole.

Underwater phases matter even more. A swimmer gliding beneath the surface faces far less drag than one swimming on top of it, which is why races are full of powerful dolphin kicks off every wall. Rules limit underwater distance to fifteen metres, and the strongest kickers use nearly all of it.

Turns, too, are a craft of their own. A good tumble turn is compact and explosive, with feet planted at precisely the right depth. Over a 1500-metre race there can be twenty-nine of them, and a tenth lost on each adds up quickly.

Finally there is the finish. Swimmers are taught to time their last stroke so that they reach the wall with arms fully extended rather than gliding in. It is a small thing, but in a sport measured in hundredths, small things are everything."""),

    ('Sports Today', "Big-Wave Surfing: Chasing the Ocean's Tallest Walls", '1502680390469-be75c86b636f', True,
     'Big-wave surfers spend months waiting for a few hours of perfect swell. When it arrives, preparation is the only thing that keeps them safe.',
     """Big-wave surfing is a sport of patience punctuated by terror. Surfers watch weather models for weeks, tracking storms thousands of kilometres away, waiting for the rare combination of swell size, wind direction and tide that turns a quiet reef into a mountain of moving water.

When the swell arrives, the margins are unforgiving. A wipeout on a wave the height of a building can hold a surfer underwater for well over a minute and push them metres beneath the surface. To prepare, big-wave athletes train their breath-holding in swimming pools, often carrying rocks along the bottom to simulate the stress of being held down.

Safety has improved dramatically. Inflatable vests can be triggered to pull a surfer to the surface, and teams of jet-ski drivers wait in the channel to pull riders out of the impact zone between sets. Many surfers say these teams are the real heroes of the sport.

Some waves are so large and fast that paddling into them is almost impossible, so surfers are towed in behind jet skis. Others are ridden by paddling alone, which purists regard as the ultimate test of skill and nerve.

Ask a big-wave surfer why they do it and the answer is rarely about adrenaline. More often it is about respect for the ocean, and about the rare, quiet clarity that comes from riding something so much bigger than yourself."""),

    ('Sports Today', 'The Tactical Art of the Peloton', '1517649763962-0c623066013b', False,
     'Professional cycling looks like a race between individuals, but it is really a moving game of chess played by teams at fifty kilometres an hour.',
     """To a casual viewer, a road race can look like a long, colourful procession. In reality, the peloton is one of the most tactically complex environments in sport.

The key is aerodynamics. A rider tucked behind others can save around thirty percent of their energy compared with riding alone at the front. That is why teams protect their leaders inside the bunch, surrounding them with teammates known as domestiques who shelter them from the wind, fetch bottles from the team car and chase down dangerous attacks.

Breakaways are another layer of strategy. Small groups often escape early in a stage, hoping the peloton will underestimate them. The chasing teams must calculate exactly how much time to allow, because pulling back a breakaway too early wastes energy, and leaving it too late can cost them the stage.

On mountain days, tactics change again. Drafting matters less at slow climbing speeds, so pure power-to-weight ratio becomes decisive. Teams try to set a pace so high that rivals' helpers are dropped one by one, leaving the opposition leader isolated.

Next time you watch a race, look beyond the rider in front. The real story is usually unfolding in the middle of the bunch."""),

    ('Politics', 'Why Local Elections Matter More Than You Think', '1555848962-6e79363ec58f', False,
     'National races grab the headlines, but the decisions that shape daily life, from schools to rubbish collection, are often made much closer to home.',
     """Turnout in local elections is often a fraction of what national contests attract. Yet the people chosen in those quieter polls make many of the decisions that most directly affect everyday life.

Local councils and county assemblies typically control land use and planning, which determines where homes, markets and roads are built. They oversee services such as waste collection, water, street lighting and public parks, and in many places they play a central role in primary education and health clinics.

Because turnout is low, every vote carries more weight. A council seat can be won or lost by a few dozen ballots, and a motivated neighbourhood group can genuinely change the outcome. That also means local representatives are often more reachable than national politicians; many hold open surgeries where residents can raise problems in person.

Local government is also a training ground. Many national leaders began their careers on a council, learning how budgets work and how to build coalitions across party lines.

If you want to make a difference without waiting years for the next national vote, the most effective place to start may be your local ballot paper, and the town hall meeting that most of your neighbours will skip."""),

    ('Technology', "What Large Language Models Can and Can't Do", '1677442136019-21780ecad995', True,
     'AI chatbots can draft emails, write code and summarise reports. Understanding how they work helps explain both their strengths and their limits.',
     """Large language models have moved from research labs into everyday tools in a remarkably short time. They help people write, summarise documents, translate text and even generate working software. But to use them well, it helps to understand what they are actually doing.

At their core, these models are trained on enormous amounts of text to predict what comes next in a sequence. Through that process they learn grammar, facts, styles of reasoning and patterns of conversation. The result can be surprisingly capable: models can follow detailed instructions, adapt their tone and explain complex ideas in plain language.

Their limits come from the same place. A model does not automatically know whether a statement is true; it produces what is plausible given its training. That is why careful users verify important facts, ask for sources and treat outputs as a strong first draft rather than a final answer.

Context is another factor. Models work best when they are given clear goals, relevant background and examples of what good output looks like. Vague requests tend to produce vague answers.

Used thoughtfully, language models can save hours of routine work and help people learn faster. The key is to treat them as a capable collaborator, one that still benefits from a human checking its work."""),

    ('Technology', 'The Global Chip Supply Chain, Explained', '1518770660439-4636190af475', False,
     'Almost every modern device depends on semiconductors, and making them involves one of the most complex supply chains ever built.',
     """The microchips inside phones, cars and data centres are the product of a supply chain that spans continents. No single country makes a modern chip from start to finish.

The journey begins with design. Engineering teams create chip architectures using specialised software, often licensing building blocks from other companies. These designs are then sent to foundries, highly specialised factories that turn silicon wafers into finished circuits.

Building a leading-edge foundry can cost tens of billions of dollars and take years. Inside, wafers pass through hundreds of steps, including the use of extreme ultraviolet lithography machines that print features thousands of times thinner than a human hair. Only a handful of companies in the world can make those machines.

After fabrication, chips are cut, tested and packaged, often in yet another country, before being shipped to device makers for assembly. A disruption at any point, from a factory fire to a shortage of specialist gases, can ripple through the entire chain.

That fragility was laid bare during recent shortages, when carmakers idled production lines for want of inexpensive chips. Governments have since invested heavily in domestic manufacturing, but experts say the industry will remain deeply interconnected for years to come."""),

    ('Technology', 'Learning to Code in 2026: Where to Start', '1488590528505-98d2b5aba04b', False,
     'With AI assistants writing code and new frameworks every month, beginners have more choice than ever. Here is a practical path through the noise.',
     """Learning to program has never been more accessible, and it has never been more overwhelming. There are thousands of courses, dozens of popular languages and a constant stream of new tools. The good news is that the fundamentals have not changed.

Start with one beginner-friendly language and stay with it. Python and JavaScript are popular choices because they have huge communities, readable syntax and countless free resources. The specific language matters less than learning core ideas such as variables, loops, functions and data structures.

Build small projects as soon as possible. A to-do list, a personal budget tracker or a simple blog teaches far more than watching tutorials passively. Projects force you to search for answers, read documentation and debug errors, which is most of what professional developers do.

AI coding assistants can be valuable teachers if used carefully. Ask them to explain code line by line, or to suggest why something is broken, rather than simply copying their answers. Understanding is the goal, not just working output.

Finally, share your work. Put projects on GitHub, join a local meet-up or an online community, and ask for feedback. Consistent practice, a few hours each week, will take you further than any single course."""),

    ('Science', 'What Earth at Night Reveals About Us', '1451187580459-43490279c0fa', False,
     'Satellite images of our planet after dark show far more than city lights. Scientists use them to track economies, disasters and even fishing fleets.',
     """Seen from orbit at night, Earth glitters with the lights of human activity. Coastlines are traced in gold, highways appear as glowing threads and great cities blaze like galaxies. These images are beautiful, but for researchers they are also a rich source of data.

Night-light data can track economic growth in places where official statistics are scarce. As towns electrify and expand, their glow grows brighter and wider, giving economists a consistent, independent measure of development.

The same data helps during emergencies. After hurricanes, earthquakes or conflicts, scientists compare before-and-after images to see where power has been lost, helping aid agencies prioritise their response.

Some of the lights are not on land at all. Fishing boats that use bright lamps to attract squid show up clearly at sea, allowing researchers to monitor fishing activity in remote waters.

There is a darker side too. Light pollution disrupts the behaviour of migrating birds, nesting sea turtles and nocturnal insects, and it hides the stars from most of humanity. Scientists hope that by mapping it carefully, cities can learn to light streets more efficiently and give the night sky back."""),

    ('Science', 'How Cancer Cells Hide From the Immune System', '1576086213369-97a306d36557', False,
     'The body is remarkably good at destroying damaged cells. Understanding how tumours slip past its defences has led to some of medicine\'s biggest breakthroughs.',
     """Every day, cells in the human body acquire mutations, and the immune system quietly destroys many of those that could become dangerous. Cancer develops when abnormal cells find ways to escape that surveillance.

One of the most important escape routes involves immune checkpoints. These are molecular brakes that normally stop immune cells from attacking healthy tissue. Some tumours exploit them by displaying signals that effectively tell immune cells to stand down.

Drugs known as checkpoint inhibitors block those signals, releasing the brakes so the immune system can attack the cancer again. For some patients with advanced melanoma, lung cancer and other diseases, these treatments have produced lasting responses that were unimaginable a generation ago.

They do not work for everyone. Some tumours have few distinctive features for the immune system to recognise, and others create a surrounding environment that suppresses immune activity. Researchers are now testing combinations of treatments, personalised vaccines and engineered immune cells to overcome these barriers.

The field is moving quickly, but the central idea is simple and powerful: rather than attacking cancer directly, help the body's own defences do the job they evolved to do."""),

    ('Travel', 'A Slow Journey Through the Italian Dolomites', '1476514525535-07fb3b4ae5f1', True,
     'Jagged peaks, emerald lakes and mountain huts serving homemade dumplings: the Dolomites reward travellers who take their time.',
     """The Dolomites rise from northern Italy like a stone cathedral, their pale limestone towers turning pink and orange at sunrise and sunset. Many visitors race between viewpoints in a single day, but the region is best experienced slowly.

Start in one of the valley towns and spend a few nights there. Mornings can be spent on gentle lake walks, where wooden rowing boats drift across water so clear it looks unreal, while afternoons are perfect for cable cars that lift you to high meadows without a punishing climb.

For more adventurous travellers, the network of mountain huts, known as rifugi, makes multi-day hikes possible without carrying a tent. Each evening ends with a hearty dinner, often including dumplings, polenta or apple strudel, shared with walkers from around the world.

The region's history adds depth to every view. Its mix of Italian, German and Ladin cultures is reflected in place names, food and architecture, and the remains of First World War fortifications can still be seen along some high trails.

Visit in early summer or September to avoid the busiest weeks, book huts well in advance and leave room in your plans for a lazy afternoon. In mountains this beautiful, the best moments are often the unplanned ones."""),

    ('Travel', 'Road-Tripping the American Southwest', '1469854523086-cc02fe5d8800', False,
     'Red rock canyons, empty desert highways and star-filled skies: how to plan an unforgettable drive through one of the world\'s great landscapes.',
     """Few journeys capture the romance of the open road like a drive through the American Southwest. The landscape changes by the hour, from towering red sandstone to sweeping desert plateaus and deep canyons carved over millions of years.

Planning is essential. Distances are long and fuel stations can be far apart, so fill up whenever you can and carry plenty of water. Summer temperatures can be extreme, which makes spring and autumn the most comfortable seasons for hiking and sightseeing.

National parks are the highlights, but popular ones can require timed-entry reservations at busy times, so check ahead. Arriving early in the morning rewards you with cooler air, softer light and far fewer people on the trails.

Leave space for the smaller stops in between: roadside diners, tiny museums and viewpoints that do not appear in guidebooks. Some of the region's most memorable experiences happen on quiet back roads.

At night, look up. With little light pollution, much of the Southwest offers some of the darkest skies in the country, and seeing the Milky Way stretch across the desert is reason enough to make the trip."""),

    ('Business', 'Reading a Market Correction Without Panicking', '1611974789855-9c2a0a7236a3', False,
     'Falling share prices make headlines and nerves jangle. Here is how long-term investors can think clearly when the market turns red.',
     """A market correction is usually defined as a fall of ten percent or more from a recent high. It sounds alarming, and the headlines often make it feel worse, but corrections are a normal part of investing and historically have happened roughly once every year or two.

The first rule is to remember your time horizon. Money you will not need for ten years or more has time to recover from short-term swings. Selling in a panic can turn a temporary paper loss into a permanent one, and investors who sell often miss the strongest days of the rebound.

Corrections can also be a moment to review rather than react. Check whether your mix of investments still matches your goals and tolerance for risk. If a fall has left your portfolio unbalanced, gradual rebalancing can help.

Regular investing smooths the ride. By putting in a fixed amount each month, you automatically buy more shares when prices are low and fewer when they are high, a strategy known as pound-cost or dollar-cost averaging.

Finally, keep an emergency fund in cash. Knowing you can cover several months of expenses without touching your investments makes it far easier to stay calm when markets wobble."""),

    ('Business', 'A Personal Budget That Actually Sticks', '1460925895917-afdab827c52f', False,
     'Most budgets fail within weeks. A few simple habits can turn a spreadsheet you dread into a plan you actually follow.',
     """Many people start the year with an ambitious budget and abandon it by February. The problem is rarely a lack of discipline; it is usually a plan that does not fit real life.

Begin by tracking what you actually spend for one month without trying to change anything. Bank apps and simple spreadsheets make this easy. The goal is an honest picture, not a perfect one.

Next, try a simple framework such as the 50/30/20 rule: roughly half of take-home pay for needs such as rent and food, thirty percent for wants and twenty percent for savings or debt repayment. The exact numbers can flex, but the structure keeps decisions simple.

Automate wherever possible. Set up transfers to savings on payday so the money moves before you have a chance to spend it, and schedule regular bills so nothing is missed.

Finally, build in fun. A budget with no room for enjoyment is a budget you will break. Allow yourself a guilt-free spending amount each month, review your progress regularly and adjust as your life changes."""),

    ('Health', 'The Ten-Minute Workout Backed by Research', '1571019613454-1cb2f99b2d8b', False,
     'No time for the gym? Short, intense bursts of exercise can deliver real health benefits, as long as you do them consistently.',
     """Lack of time is one of the most common reasons people give for not exercising. The encouraging news from sports science is that even short workouts can make a measurable difference.

High-intensity interval training, often shortened to HIIT, alternates brief periods of hard effort with short recoveries. Studies have found that sessions lasting ten to twenty minutes can improve cardiovascular fitness and blood sugar control, particularly in people who were previously inactive.

A simple routine might include jumping jacks, bodyweight squats, push-ups and mountain climbers, each performed for forty seconds followed by twenty seconds of rest, repeated twice. No equipment is needed, and it can be done in a living room.

Intensity is relative. For a beginner, a brisk walk up a hill may be high-intensity, and that is fine. The key is to work hard enough that talking becomes difficult during each interval, then recover fully.

Short workouts are not a complete substitute for an active lifestyle, and health guidelines still recommend regular movement throughout the week. But on busy days, ten focused minutes is far better than nothing, and it might be the habit that sticks."""),

    ('Health', 'What a Mediterranean Plate Really Looks Like', '1490645935967-10de6ba17061', False,
     'The Mediterranean diet is consistently ranked among the healthiest in the world. It is less about strict rules and more about a way of eating.',
     """The Mediterranean diet has been studied for decades and is consistently linked to lower risks of heart disease and other chronic conditions. Despite its reputation, it is not a strict plan with forbidden foods. It is a pattern of eating inspired by traditional cooking around the Mediterranean Sea.

Vegetables, fruit, whole grains and legumes form the foundation of most meals. Olive oil is the main source of fat, used generously for cooking and dressing salads. Nuts and seeds appear as snacks, and herbs and spices add flavour in place of excess salt.

Fish and seafood are eaten regularly, while poultry, eggs and dairy appear in moderate amounts. Red meat and sweets are enjoyed occasionally rather than daily.

A typical plate might include a large salad with chickpeas and olive oil, a piece of grilled fish, a portion of whole-grain bread and a handful of fresh fruit for dessert. Simple, seasonal and satisfying.

Just as important is how food is eaten. Traditional Mediterranean meals are often shared slowly with family and friends, and researchers increasingly believe that social connection may be part of the diet's benefits."""),

    ('Entertainment', 'Why Live Music Still Feels Different', '1470229722913-7c0e2dbbafd3', False,
     'Streaming puts millions of songs in our pockets, yet concert tickets keep selling out. What is it about hearing music in a crowd?',
     """In an age when almost any song can be streamed instantly, more people than ever are paying to see music performed live. Festivals sell out months in advance and arena tours break attendance records. So what is the draw?

Part of it is physical. At a concert, music is not just heard but felt: the bass vibrates through the floor and the volume fills the body in a way headphones cannot reproduce.

Part of it is social. Researchers have found that when people experience music together, their heart rates and movements can begin to synchronise. Singing along with thousands of strangers creates a powerful sense of belonging that is hard to find elsewhere.

There is also the thrill of the unrepeatable. A live show can include new arrangements, unexpected guests, mistakes and moments of spontaneity. Fans know they are witnessing something that will never happen in quite the same way again.

For artists, live performance has become an essential source of income as streaming pays relatively little per play. For audiences, it remains one of the purest forms of shared joy."""),

    ('Entertainment', 'The Quiet Return of the Neighbourhood Cinema', '1489599849927-2ee91cede3ba', False,
     'Small independent cinemas were written off in the streaming era. Many are now thriving by offering something a sofa cannot.',
     """When streaming services exploded, many predicted the end of the small cinema. Why travel and pay for a ticket when thousands of films are available at home? Yet in towns and cities around the world, independent picture houses are finding new audiences.

Their secret is experience. Many have restored historic buildings, added comfortable seating and opened cafes and bars where audiences linger before and after screenings. A trip to the cinema has become a night out rather than simply a way to watch a film.

Programming is another strength. Independent cinemas show classics, foreign-language films, documentaries and local productions that rarely appear in large multiplexes. Themed seasons, director talks and community screenings give people a reason to return.

Some venues have become cultural hubs, hosting film clubs, school screenings and festivals. Others offer relaxed screenings for families with young children or people with sensory sensitivities.

The lesson is that people still crave shared experiences. A good film watched in the dark among strangers, laughing and gasping together, remains one of life's small pleasures."""),
]

EXISTING_IMAGES = {
    'soccer-afcon-senegal-and-morocco-fines-caf': '1431324155629-1a6deb1dec8d',
    'tennis-vlada-hranchar-ukraine-prodigy': '1622279457486-62dcc4a431d6',
    'kenyas-202526-fiscal-choices-and-the-future-of-civic-space': '1554224155-6726b3ff858f',
    '30-years-of-world-politics-what-has-changed': '1529107386315-e1a2ed48a620',
    'how-iphones-made-a-surprising-comeback-in-china': '1511707171634-5f897ff02aa9',
    'technology-the-good-the-bad-the-ugly': '1550751827-4bd374c3f58b',
}

NEW_CATEGORIES = ['Business', 'Health', 'Entertainment']


class Command(BaseCommand):
    help = 'Adds sample blog posts with Unsplash images (safe to run more than once).'

    def handle(self, *args, **options):
        author = User.objects.filter(is_superuser=True).first() or User.objects.first()
        if author is None:
            self.stderr.write('Create a user first: python manage.py createsuperuser')
            return

        for name in NEW_CATEGORIES:
            Category.objects.get_or_create(category_name=name)

        # existing posts: give them an image to fall back on if the uploaded file is missing
        for slug, pid in EXISTING_IMAGES.items():
            Blog.objects.filter(slug=slug, image_url='').update(image_url=UNSPLASH.format(pid))

        now = timezone.now()
        created = 0
        for i, (cat, title, pid, featured, short, body) in enumerate(POSTS):
            category, _ = Category.objects.get_or_create(category_name=cat)
            post, is_new = Blog.objects.get_or_create(
                title=title,
                defaults=dict(
                    category=category,
                    author=author,
                    image_url=UNSPLASH.format(pid),
                    short_description=short,
                    blog_body=body,
                    status='Published',
                    is_featured=featured,
                    views=(len(POSTS) - i) * 37 % 500 + 40,
                ),
            )
            if is_new:
                created += 1
                # stagger publish times so "x hours ago" looks natural
                Blog.objects.filter(pk=post.pk).update(created_at=now - timedelta(hours=i * 3 + 1))

        About.objects.get_or_create(
            defaults=dict(
                about_heading='About Me:',
                about_description='Practical insights on sport, technology, travel and life, with clear explanations and lessons learned along the way.',
            )
        )
        self.stdout.write(self.style.SUCCESS(f'Done. {created} new posts added, {Blog.objects.count()} posts in total.'))
