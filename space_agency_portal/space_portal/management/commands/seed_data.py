"""
Management command to seed sample data into the database.
Run: python manage.py seed_data
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils.text import slugify
from space_portal.models import Mission, Astronaut, Launch, NewsArticle, SpacecraftGallery
from datetime import date, timedelta
from django.utils import timezone
import random


class Command(BaseCommand):
    help = 'Seeds the database with sample space agency data'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING('🚀 Seeding COSMOSX database...'))

        # Create superuser
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_superuser('admin', 'admin@cosmosx.space', 'admin123')
            admin.first_name = 'Mission'
            admin.last_name = 'Control'
            admin.save()
            self.stdout.write(self.style.SUCCESS('  ✓ Admin user created (admin / admin123)'))

        author = User.objects.get(username='admin')

        # ── Missions ──
        missions_data = [
            {
                'name': 'Artemis Prime', 'mission_type': 'lunar', 'status': 'active',
                'launch_date': date(2024, 3, 15), 'description': 'The landmark return to lunar orbit — establishing humanity\'s sustained presence on and around the Moon. Artemis Prime carries a crew of four on a 28-day mission to test habitation systems, conduct geological surveys, and deploy a lunar gateway module.',
                'objectives': 'Establish lunar orbit communications relay. Conduct geological surveys of polar region. Test long-duration life support systems. Deploy navigation beacons for future surface missions.',
                'crew_count': 4,
            },
            {
                'name': 'Mars Horizon I', 'mission_type': 'mars', 'status': 'active',
                'launch_date': date(2024, 7, 22), 'description': 'First crewed mission to Mars orbit — a historic 420-day journey carrying six astronauts on humanity\'s greatest adventure. The crew will conduct extensive remote sensing, deploy surface probes, and prepare for eventual surface landings.',
                'objectives': 'Achieve stable Mars orbit. Deploy autonomous surface rovers. Map subsurface water ice deposits. Assess radiation environment for future surface missions. Test in-situ resource utilization technology.',
                'crew_count': 6,
            },
            {
                'name': 'Orbital Lab 7', 'mission_type': 'orbit', 'status': 'active',
                'launch_date': date(2024, 1, 10), 'description': 'Extended low-Earth orbit research laboratory mission aboard the COSMOSX Space Station. Crew conducts 200+ scientific experiments across biology, physics, materials science, and Earth observation.',
                'objectives': 'Run 200 scientific experiments. Test new space construction techniques. Monitor climate indicators. Develop microgravity manufacturing processes.',
                'crew_count': 3,
            },
            {
                'name': 'Europa Pathfinder', 'mission_type': 'deep_space', 'status': 'planned',
                'launch_date': date(2026, 9, 1), 'description': 'Robotic precursor mission to Jupiter\'s moon Europa. Europa Pathfinder will perform close flybys, analyze the subsurface ocean chemistry, and scout landing sites for a future life-detection mission.',
                'objectives': 'Map Europa\'s surface in high resolution. Sample plume material from subsurface ocean. Search for biosignatures. Characterize radiation environment.',
                'crew_count': 0,
            },
            {
                'name': 'Titan Surveyor', 'mission_type': 'deep_space', 'status': 'planned',
                'launch_date': date(2027, 4, 15), 'description': 'An aerial drone mission to Saturn\'s moon Titan — exploring the haze-shrouded world of methane lakes and complex organic chemistry that may mirror early Earth conditions.',
                'objectives': 'Aerial survey of Titan\'s methane lakes. Atmospheric chemistry sampling. Search for prebiotic molecules. Deploy seismic sensors.',
                'crew_count': 0,
            },
            {
                'name': 'ISS Resupply X-12', 'mission_type': 'iss', 'status': 'completed',
                'launch_date': date(2023, 5, 3), 'end_date': date(2023, 5, 10), 'description': 'Successful cargo resupply mission delivering 3.5 tons of supplies, scientific equipment, and replacement hardware to the International Space Station.',
                'objectives': 'Deliver 3.5 tons of cargo. Replace life support components. Deliver new scientific experiments. Return samples to Earth.',
                'crew_count': 2,
            },
            {
                'name': 'Lunar Gateway Alpha', 'mission_type': 'lunar', 'status': 'planned',
                'launch_date': date(2026, 2, 14), 'description': 'Construction mission to assemble the core module of the Lunar Gateway — a permanent space station orbiting the Moon that will serve as a hub for lunar surface and deep space missions.',
                'objectives': 'Launch and dock core habitation module. Activate power and propulsion system. Test communications relay to Earth and lunar surface.',
                'crew_count': 4,
            },
            {
                'name': 'Earth Observer VII', 'mission_type': 'satellite', 'status': 'completed',
                'launch_date': date(2022, 11, 20), 'end_date': date(2023, 11, 20), 'description': 'Advanced Earth observation satellite mission providing high-resolution climate monitoring, disaster response support, and agricultural data to 190 partner nations.',
                'objectives': 'Deploy climate monitoring instruments. Provide disaster response imagery. Monitor polar ice sheets. Track deforestation patterns.',
                'crew_count': 0,
            },
        ]

        missions = []
        for data in missions_data:
            end_date = data.pop('end_date', None)
            slug = slugify(data['name'])
            mission, created = Mission.objects.get_or_create(
                slug=slug,
                defaults={**data, 'end_date': end_date, 'agency': 'COSMOSX Agency'}
            )
            missions.append(mission)
            if created:
                self.stdout.write(f'  ✓ Mission: {mission.name}')

        # ── Astronauts ──
        astronauts_data = [
            {
                'name': 'Commander Elena Vasquez', 'nationality': 'American', 'status': 'active',
                'bio': 'Commander Vasquez is a decorated test pilot and mission commander with 3 spaceflights totaling over 400 hours in space. A veteran of two ISS expeditions, she was selected to command the historic Mars Horizon I mission. With degrees in aerospace engineering and astrobiology, she embodies the multi-disciplinary spirit of modern space exploration.',
                'missions_count': 3, 'hours_in_space': 412.5, 'rank': 'Commander',
                'specialization': 'Mission Command & Aerospace Engineering',
            },
            {
                'name': 'Dr. Kenji Tanaka', 'nationality': 'Japanese', 'status': 'active',
                'bio': 'Dr. Tanaka is a physician-astronaut and biologist who has spent more cumulative time in microgravity than any other COSMOSX crew member. His research on long-duration spaceflight physiology has directly improved health protocols for future Mars missions.',
                'missions_count': 4, 'hours_in_space': 620.0, 'rank': 'Flight Surgeon',
                'specialization': 'Space Medicine & Biology',
            },
            {
                'name': 'Flight Engineer Amara Osei', 'nationality': 'Ghanaian', 'status': 'active',
                'bio': 'A pioneering figure as one of Africa\'s first deep-space-qualified astronauts, Flight Engineer Osei specializes in propulsion systems and EVA operations. Her expertise in advanced orbital mechanics was instrumental in planning the Europa Pathfinder trajectory.',
                'missions_count': 2, 'hours_in_space': 280.0, 'rank': 'Flight Engineer',
                'specialization': 'Propulsion & EVA Operations',
            },
            {
                'name': 'Dr. Mikhail Petrov', 'nationality': 'Russian', 'status': 'active',
                'bio': 'Dr. Petrov is a geologist and planetary scientist with a passion for extraterrestrial geology. Having participated in Arctic and Antarctic field research as analog studies, he brings unique expertise to lunar and Martian surface mission planning.',
                'missions_count': 2, 'hours_in_space': 190.0, 'rank': 'Mission Specialist',
                'specialization': 'Planetary Geology & Remote Sensing',
            },
            {
                'name': 'Pilot Sara Chen', 'nationality': 'Canadian', 'status': 'active',
                'bio': 'One of the youngest pilots ever certified for crewed deep-space missions, Pilot Chen holds records in multiple flight categories. Her precision during the Artemis Prime trans-lunar injection burn was celebrated as textbook perfect.',
                'missions_count': 1, 'hours_in_space': 95.0, 'rank': 'Pilot',
                'specialization': 'Spacecraft Piloting & Navigation',
            },
            {
                'name': 'Astronaut James Park', 'nationality': 'South Korean', 'status': 'training',
                'bio': 'Currently completing advanced EVA and Mars surface simulation training, James Park represents the next generation of COSMOSX explorers. His background in robotics engineering and AI will be invaluable for autonomous systems management on future missions.',
                'missions_count': 0, 'hours_in_space': 0.0, 'rank': 'Mission Specialist (Trainee)',
                'specialization': 'Robotics & Artificial Intelligence',
            },
            {
                'name': 'Dr. Fatima Al-Rashid', 'nationality': 'Saudi Arabian', 'status': 'active',
                'bio': 'Dr. Al-Rashid is an astrophysicist who conducts cutting-edge dark matter research aboard the orbital laboratory. Her observational work with the COSMOSX space telescope has led to two significant discoveries in exoplanet atmospheric chemistry.',
                'missions_count': 2, 'hours_in_space': 350.0, 'rank': 'Science Officer',
                'specialization': 'Astrophysics & Telescope Operations',
            },
            {
                'name': 'Col. Robert Hughes', 'nationality': 'British', 'status': 'retired',
                'bio': 'Colonel Hughes served COSMOSX for 18 distinguished years, commanding five missions and setting the agency record for EVA hours. His leadership during the Orbital Lab 4 emergency prevented the loss of the station and saved three lives. Now retired, he serves as senior advisor for mission safety.',
                'missions_count': 5, 'hours_in_space': 890.0, 'rank': 'Colonel (Ret.)',
                'specialization': 'Mission Safety & EVA',
            },
        ]

        for i, data in enumerate(astronauts_data):
            astronaut, created = Astronaut.objects.get_or_create(
                name=data['name'],
                defaults={**data, 'birth_date': date(1970 + i*3, 4 + i, 10 + i)}
            )
            # Assign missions
            if astronaut.status == 'active' and missions:
                astronaut.missions.set(random.sample(missions[:5], min(data['missions_count'], len(missions[:5]))))
            if created:
                self.stdout.write(f'  ✓ Astronaut: {astronaut.name}')

        # ── Launches ──
        launches_data = [
            {
                'mission': missions[0], 'rocket_name': 'Cosmos Heavy V', 'launch_site': 'Kennedy Space Center, FL',
                'launch_datetime': timezone.now() + timedelta(days=45), 'status': 'scheduled',
                'notes': 'Crew of 4 bound for lunar orbit on 28-day mission.',
            },
            {
                'mission': missions[1], 'rocket_name': 'Titan Ultra', 'launch_site': 'Vandenberg SFB, CA',
                'launch_datetime': timezone.now() + timedelta(days=120), 'status': 'scheduled',
                'notes': 'Historic first crewed Mars mission. 420-day round trip.',
            },
            {
                'mission': missions[3], 'rocket_name': 'StarRocket X', 'launch_site': 'Boca Chica, TX',
                'launch_datetime': timezone.now() + timedelta(days=600), 'status': 'scheduled',
                'notes': 'Robotic precursor to Europa. 6-year transit time.',
            },
            {
                'mission': missions[5], 'rocket_name': 'Cosmos Medium III', 'launch_site': 'Kennedy Space Center, FL',
                'launch_datetime': timezone.now() - timedelta(days=720), 'status': 'launched',
                'notes': 'Successful resupply mission completed.',
            },
        ]

        for data in launches_data:
            launch, created = Launch.objects.get_or_create(
                mission=data['mission'],
                rocket_name=data['rocket_name'],
                defaults=data
            )
            if created:
                self.stdout.write(f'  ✓ Launch: {launch.rocket_name}')

        # ── News Articles ──
        articles_data = [
            {
                'title': 'Mars Horizon I Crew Completes Final Pre-Launch Training',
                'category': 'mission', 'is_featured': True,
                'summary': 'The six-person Mars Horizon I crew has successfully completed their final integrated simulation, clearing the last major milestone before launch day.',
                'content': 'The crew of Mars Horizon I — humanity\'s first crewed mission to Mars orbit — has completed all pre-launch training requirements ahead of their historic departure. Over the past 18 months, the team has trained extensively in underwater EVA simulations, habitat systems management, emergency protocols, and psychological resilience programs.\n\nCommander Elena Vasquez expressed confidence: "This team is ready. We\'ve trained for every scenario we can imagine, and then some. The years of preparation culminate in this mission."\n\nThe crew will spend 420 days in space, including 90 days in Mars orbit conducting remote sensing operations, deploying autonomous rovers, and preparing the groundwork for eventual crewed landings. Their spacecraft, the COSMOSX Ares, features next-generation ion propulsion and closed-loop life support systems capable of 500+ days of autonomous operation.\n\nLaunch is scheduled for the upcoming Mars transfer window, which opens in approximately 120 days. Mission Control will conduct final system checks and launch rehearsals in the intervening period.',
            },
            {
                'title': 'Artemis Prime Discovers Water Ice in Lunar South Pole',
                'category': 'research', 'is_featured': True,
                'summary': 'Ground-penetrating radar data from Artemis Prime confirms substantial deposits of water ice in permanently shadowed craters near the lunar south pole — a game-changer for future surface missions.',
                'content': 'In a discovery that could transform the future of lunar exploration, the Artemis Prime crew has confirmed the presence of substantial water ice deposits using the onboard ground-penetrating radar system. The deposits, located in permanently shadowed craters near the lunar south pole, appear to be far more extensive than previously estimated.\n\nDr. Mikhail Petrov, mission geologist, described the finding: "The radar returns are unambiguous. We are looking at deposits that could supply water, oxygen, and hydrogen propellant for many future missions. This is the discovery that makes a permanent lunar presence genuinely feasible."\n\nThe water ice, estimated to extend to depths of several meters, was likely delivered by cometary impacts over billions of years and preserved in the extreme cold of permanently shadowed regions where temperatures reach -250°C. Scientists estimate that the detected deposits could sustain a crew of eight for decades if properly extracted.',
            },
            {
                'title': 'New Space Suit Technology Extends EVA Duration by 40%',
                'category': 'technology', 'is_featured': True,
                'summary': 'COSMOSX\'s Advanced Extravehicular Mobility Unit introduces revolutionary thermal regulation and oxygen recycling that dramatically extends spacewalk capability.',
                'content': 'COSMOSX engineers have unveiled the next-generation Extravehicular Mobility Unit (EMU-X), a radical redesign that extends safe EVA duration from 8 hours to over 12 hours. The breakthrough comes from two key innovations: a closed-loop oxygen recycling system that reduces consumable mass by 60%, and a phase-change thermal regulation system that maintains suit temperature within 1°C regardless of solar conditions.\n\nThe suit also features enhanced joint mobility inspired by biomechanical research, reducing crew fatigue by an estimated 35%. Integrated health monitoring continuously tracks vital signs, detecting early signs of decompression sickness or hypoxia before they become dangerous.\n\nPilot Sara Chen, who tested the prototype during Orbital Lab 7 EVAs, said the difference was immediately apparent: "You feel less like you\'re fighting the suit and more like it\'s an extension of your body. The thermal control especially — you stop thinking about heat and cold entirely."\n\nThe EMU-X will be standard equipment for all COSMOSX missions from 2025 onward, beginning with the Lunar Gateway Alpha construction mission.',
            },
            {
                'title': 'COSMOSX Announces Partnership with ESA for Titan Mission',
                'category': 'general', 'is_featured': False,
                'summary': 'A landmark partnership with the European Space Agency will see joint development of the Titan Surveyor drone, pooling expertise from both agencies for this ambitious outer planet mission.',
                'content': 'COSMOSX and the European Space Agency have signed a comprehensive partnership agreement for the Titan Surveyor mission, combining resources, expertise, and funding for what will be the most technically complex robotic mission in history.\n\nUnder the agreement, ESA will contribute the nuclear-powered radioisotope thermoelectric generator and atmospheric science instruments, while COSMOSX provides the rotorcraft platform, communications systems, and mission management. The collaboration represents a combined investment of $3.2 billion over 15 years.\n\nThe Titan Surveyor will spend approximately three years flying through the thick atmosphere of Saturn\'s largest moon, covering thousands of kilometers of terrain from the methane seas of the north to the hydrocarbon dune fields of the equatorial regions.',
            },
            {
                'title': 'Astronaut Kenji Tanaka Breaks Duration Record',
                'category': 'astronaut', 'is_featured': False,
                'summary': 'Dr. Kenji Tanaka has surpassed 620 hours in space across four missions, setting a new COSMOSX record for cumulative time in microgravity.',
                'content': 'Dr. Kenji Tanaka has achieved a significant personal and agency milestone, accumulating over 620 hours in space across his four COSMOSX missions — more than any other crew member in the agency\'s 24-year history.\n\nThe record was marked during his ongoing assignment aboard Orbital Lab 7, where Tanaka is leading a suite of experiments on bone density preservation during long-duration spaceflight. His own physiology has become part of the research dataset, with extensive medical monitoring providing invaluable data for planning future Mars missions.\n\n"Every hour I spend up here, I learn something that will help the people coming after me," Tanaka said in a statement from orbit. "The real record I want to help break is the distance from Earth when humans land on Mars."\n\nMission Director Carlos Reyes praised Tanaka\'s contributions: "Kenji is not just a record holder — he\'s a foundational pillar of our understanding of how the human body adapts to space."',
            },
        ]

        for data in articles_data:
            slug = slugify(data['title'])[:100]
            article, created = NewsArticle.objects.get_or_create(
                slug=slug,
                defaults={**data, 'author': author}
            )
            if created:
                self.stdout.write(f'  ✓ Article: {article.title[:50]}...')

        # ── Spacecraft ──
        spacecraft_data = [
            {'name': 'Cosmos Heavy V', 'spacecraft_type': 'Heavy Lift Rocket', 'manufacturer': 'COSMOSX Launch Division', 'description': 'The workhorse of COSMOSX crewed missions. Cosmos Heavy V delivers up to 70 metric tons to low-Earth orbit and 25 metric tons to trans-lunar injection. It has flown 28 consecutive successful missions.', 'first_flight': date(2019, 6, 10)},
            {'name': 'COSMOSX Ares', 'spacecraft_type': 'Crewed Spacecraft', 'manufacturer': 'COSMOSX Vehicle Systems', 'description': 'Next-generation crewed spacecraft designed for deep space missions up to 500 days. Features redundant life support, advanced radiation shielding, and ion propulsion for Mars transit.', 'first_flight': date(2023, 3, 15)},
            {'name': 'Titan Ultra', 'spacecraft_type': 'Super Heavy Rocket', 'manufacturer': 'COSMOSX Launch Division', 'description': 'The most powerful rocket in the COSMOSX fleet. Titan Ultra delivers 150 metric tons to LEO and is designed for direct Mars injection of fully fueled interplanetary spacecraft.', 'first_flight': date(2022, 11, 1)},
            {'name': 'COSMOSX Habitat Module', 'spacecraft_type': 'Space Station Module', 'manufacturer': 'COSMOSX Life Systems', 'description': 'Inflatable habitat module providing 330 cubic meters of pressurized living space. Used aboard the COSMOSX Space Station and designed for the Lunar Gateway.', 'first_flight': date(2021, 8, 20)},
            {'name': 'Europa Lander Concept', 'spacecraft_type': 'Robotic Lander', 'manufacturer': 'COSMOSX Robotics Lab', 'description': 'Proposed robotic lander for Europa\'s icy surface. Features a heated drill capable of penetrating 5km of ice to reach the subsurface ocean. Currently in Phase B development.', 'first_flight': None},
            {'name': 'Titan Surveyor Drone', 'spacecraft_type': 'Aerial Drone', 'manufacturer': 'COSMOSX / ESA Joint', 'description': 'Nuclear-powered rotorcraft designed to fly through Titan\'s thick nitrogen-methane atmosphere. Eight coaxial rotors provide lift in atmospheric conditions 4x denser than Earth\'s at surface level.', 'first_flight': None},
        ]

        for data in spacecraft_data:
            craft, created = SpacecraftGallery.objects.get_or_create(
                name=data['name'], defaults=data
            )
            if created:
                self.stdout.write(f'  ✓ Spacecraft: {craft.name}')

        self.stdout.write(self.style.SUCCESS('\n✅ Database seeded successfully!'))
        self.stdout.write(self.style.SUCCESS('   Admin login: admin / admin123'))
        self.stdout.write(self.style.SUCCESS('   Visit http://127.0.0.1:8000/ to view the portal'))
        self.stdout.write(self.style.SUCCESS('   Admin panel: http://127.0.0.1:8000/admin/'))
