"""
Build Canonical SDG Reference Data (Goals 1-17 and Official Targets).
Grounds M5 in official United Nations Sustainable Development Goals framework.
"""
import os
import json

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SDG_DIR = os.path.join(PROJECT_ROOT, "data", "sdg")
os.makedirs(SDG_DIR, exist_ok=True)

SDG_GOALS = [
    {
        "sdg_id": "SDG_01",
        "sdg_number": 1,
        "official_name": "No Poverty",
        "official_summary": "End poverty in all its forms everywhere.",
        "official_source_url": "https://sdgs.un.org/goals/goal1",
        "last_verified_date": "2026-10-24"
    },
    {
        "sdg_id": "SDG_02",
        "sdg_number": 2,
        "official_name": "Zero Hunger",
        "official_summary": "End hunger, achieve food security and improved nutrition and promote sustainable agriculture.",
        "official_source_url": "https://sdgs.un.org/goals/goal2",
        "last_verified_date": "2026-10-24"
    },
    {
        "sdg_id": "SDG_03",
        "sdg_number": 3,
        "official_name": "Good Health and Well-Being",
        "official_summary": "Ensure healthy lives and promote well-being for all at all ages.",
        "official_source_url": "https://sdgs.un.org/goals/goal3",
        "last_verified_date": "2026-10-24"
    },
    {
        "sdg_id": "SDG_04",
        "sdg_number": 4,
        "official_name": "Quality Education",
        "official_summary": "Ensure inclusive and equitable quality education and promote lifelong learning opportunities for all.",
        "official_source_url": "https://sdgs.un.org/goals/goal4",
        "last_verified_date": "2026-10-24"
    },
    {
        "sdg_id": "SDG_05",
        "sdg_number": 5,
        "official_name": "Gender Equality",
        "official_summary": "Achieve gender equality and empower all women and girls.",
        "official_source_url": "https://sdgs.un.org/goals/goal5",
        "last_verified_date": "2026-10-24"
    },
    {
        "sdg_id": "SDG_06",
        "sdg_number": 6,
        "official_name": "Clean Water and Sanitation",
        "official_summary": "Ensure availability and sustainable management of water and sanitation for all.",
        "official_source_url": "https://sdgs.un.org/goals/goal6",
        "last_verified_date": "2026-10-24"
    },
    {
        "sdg_id": "SDG_07",
        "sdg_number": 7,
        "official_name": "Affordable and Clean Energy",
        "official_summary": "Ensure access to affordable, reliable, sustainable and modern energy for all.",
        "official_source_url": "https://sdgs.un.org/goals/goal7",
        "last_verified_date": "2026-10-24"
    },
    {
        "sdg_id": "SDG_08",
        "sdg_number": 8,
        "official_name": "Decent Work and Economic Growth",
        "official_summary": "Promote sustained, inclusive and sustainable economic growth, full and productive employment and decent work for all.",
        "official_source_url": "https://sdgs.un.org/goals/goal8",
        "last_verified_date": "2026-10-24"
    },
    {
        "sdg_id": "SDG_09",
        "sdg_number": 9,
        "official_name": "Industry, Innovation and Infrastructure",
        "official_summary": "Build resilient infrastructure, promote inclusive and sustainable industrialization and foster innovation.",
        "official_source_url": "https://sdgs.un.org/goals/goal9",
        "last_verified_date": "2026-10-24"
    },
    {
        "sdg_id": "SDG_10",
        "sdg_number": 10,
        "official_name": "Reduced Inequalities",
        "official_summary": "Reduce inequality within and among countries.",
        "official_source_url": "https://sdgs.un.org/goals/goal10",
        "last_verified_date": "2026-10-24"
    },
    {
        "sdg_id": "SDG_11",
        "sdg_number": 11,
        "official_name": "Sustainable Cities and Communities",
        "official_summary": "Make cities and human settlements inclusive, safe, resilient and sustainable.",
        "official_source_url": "https://sdgs.un.org/goals/goal11",
        "last_verified_date": "2026-10-24"
    },
    {
        "sdg_id": "SDG_12",
        "sdg_number": 12,
        "official_name": "Responsible Consumption and Production",
        "official_summary": "Ensure sustainable consumption and production patterns.",
        "official_source_url": "https://sdgs.un.org/goals/goal12",
        "last_verified_date": "2026-10-24"
    },
    {
        "sdg_id": "SDG_13",
        "sdg_number": 13,
        "official_name": "Climate Action",
        "official_summary": "Take urgent action to combat climate change and its impacts.",
        "official_source_url": "https://sdgs.un.org/goals/goal13",
        "last_verified_date": "2026-10-24"
    },
    {
        "sdg_id": "SDG_14",
        "sdg_number": 14,
        "official_name": "Life Below Water",
        "official_summary": "Conserve and sustainably use the oceans, seas and marine resources for sustainable development.",
        "official_source_url": "https://sdgs.un.org/goals/goal14",
        "last_verified_date": "2026-10-24"
    },
    {
        "sdg_id": "SDG_15",
        "sdg_number": 15,
        "official_name": "Life on Land",
        "official_summary": "Protect, restore and promote sustainable use of terrestrial ecosystems, sustainably manage forests, combat desertification, and halt and reverse land degradation and halt biodiversity loss.",
        "official_source_url": "https://sdgs.un.org/goals/goal15",
        "last_verified_date": "2026-10-24"
    },
    {
        "sdg_id": "SDG_16",
        "sdg_number": 16,
        "official_name": "Peace, Justice and Strong Institutions",
        "official_summary": "Promote peaceful and inclusive societies for sustainable development, provide access to justice for all and build effective, accountable and inclusive institutions at all levels.",
        "official_source_url": "https://sdgs.un.org/goals/goal16",
        "last_verified_date": "2026-10-24"
    },
    {
        "sdg_id": "SDG_17",
        "sdg_number": 17,
        "official_name": "Partnerships for the Goals",
        "official_summary": "Strengthen the means of implementation and revitalize the Global Partnership for Sustainable Development.",
        "official_source_url": "https://sdgs.un.org/goals/goal17",
        "last_verified_date": "2026-10-24"
    }
]

SDG_TARGETS = [
    {
        "target_id": "4.4",
        "sdg_number": 4,
        "official_target_text": "By 2030, substantially increase the number of youth and adults who have relevant skills, including technical and vocational skills, for employment, decent jobs and entrepreneurship.",
        "target_short_label": "Relevant Skills for Employment",
        "source_url": "https://sdgs.un.org/goals/goal4#targets-and-indicators",
        "last_verified_date": "2026-10-24"
    },
    {
        "target_id": "4.7",
        "sdg_number": 4,
        "official_target_text": "By 2030, ensure that all learners acquire the knowledge and skills needed to promote sustainable development, including, among others, through education for sustainable development and sustainable lifestyles...",
        "target_short_label": "Education for Sustainable Development",
        "source_url": "https://sdgs.un.org/goals/goal4#targets-and-indicators",
        "last_verified_date": "2026-10-24"
    },
    {
        "target_id": "7.1",
        "sdg_number": 7,
        "official_target_text": "By 2030, ensure universal access to affordable, reliable and modern energy services.",
        "target_short_label": "Universal Modern Energy Access",
        "source_url": "https://sdgs.un.org/goals/goal7#targets-and-indicators",
        "last_verified_date": "2026-10-24"
    },
    {
        "target_id": "7.2",
        "sdg_number": 7,
        "official_target_text": "By 2030, increase substantially the share of renewable energy in the global energy mix.",
        "target_short_label": "Increase Renewable Energy Share",
        "source_url": "https://sdgs.un.org/goals/goal7#targets-and-indicators",
        "last_verified_date": "2026-10-24"
    },
    {
        "target_id": "7.3",
        "sdg_number": 7,
        "official_target_text": "By 2030, double the global rate of improvement in energy efficiency.",
        "target_short_label": "Double Energy Efficiency Rate",
        "source_url": "https://sdgs.un.org/goals/goal7#targets-and-indicators",
        "last_verified_date": "2026-10-24"
    },
    {
        "target_id": "8.2",
        "sdg_number": 8,
        "official_target_text": "Achieve higher levels of economic productivity through diversification, technological upgrading and innovation, including through a focus on high-value added and labour-intensive sectors.",
        "target_short_label": "Productivity & Tech Upgrading",
        "source_url": "https://sdgs.un.org/goals/goal8#targets-and-indicators",
        "last_verified_date": "2026-10-24"
    },
    {
        "target_id": "8.5",
        "sdg_number": 8,
        "official_target_text": "By 2030, achieve full and productive employment and decent work for all women and men, including for young people and persons with disabilities, and equal pay for work of equal value.",
        "target_short_label": "Full Productive Employment & Decent Work",
        "source_url": "https://sdgs.un.org/goals/goal8#targets-and-indicators",
        "last_verified_date": "2026-10-24"
    },
    {
        "target_id": "8.8",
        "sdg_number": 8,
        "official_target_text": "Protect labour rights and promote safe and secure working environments for all workers, including migrant workers, in particular women migrants, and those in precarious employment.",
        "target_short_label": "Safe Working Environments & Rights",
        "source_url": "https://sdgs.un.org/goals/goal8#targets-and-indicators",
        "last_verified_date": "2026-10-24"
    },
    {
        "target_id": "9.1",
        "sdg_number": 9,
        "official_target_text": "Develop quality, reliable, sustainable and resilient infrastructure, including regional and transborder infrastructure, to support economic development and human well-being...",
        "target_short_label": "Resilient Quality Infrastructure",
        "source_url": "https://sdgs.un.org/goals/goal9#targets-and-indicators",
        "last_verified_date": "2026-10-24"
    },
    {
        "target_id": "9.4",
        "sdg_number": 9,
        "official_target_text": "By 2030, upgrade infrastructure and retrofit industries to make them sustainable, with increased resource-use efficiency and greater adoption of clean and environmentally sound technologies and industrial processes...",
        "target_short_label": "Upgrade Sustainable Industrial Processes",
        "source_url": "https://sdgs.un.org/goals/goal9#targets-and-indicators",
        "last_verified_date": "2026-10-24"
    },
    {
        "target_id": "9.5",
        "sdg_number": 9,
        "official_target_text": "Enhance scientific research, upgrade the technological capabilities of industrial sectors in all countries, in particular developing countries, including, by 2030, encouraging innovation and substantially increasing the number of research and development workers...",
        "target_short_label": "Enhance Scientific Research & R&D",
        "source_url": "https://sdgs.un.org/goals/goal9#targets-and-indicators",
        "last_verified_date": "2026-10-24"
    },
    {
        "target_id": "9.c",
        "sdg_number": 9,
        "official_target_text": "Significantly increase access to information and communications technology and strive to provide universal and affordable access to the Internet in least developed countries by 2020.",
        "target_short_label": "Universal ICT & Internet Access",
        "source_url": "https://sdgs.un.org/goals/goal9#targets-and-indicators",
        "last_verified_date": "2026-10-24"
    },
    {
        "target_id": "10.2",
        "sdg_number": 10,
        "official_target_text": "By 2030, empower and promote the social, economic and political inclusion of all, irrespective of age, sex, disability, race, ethnicity, origin, religion or economic or other status.",
        "target_short_label": "Promote Socio-Economic Inclusion",
        "source_url": "https://sdgs.un.org/goals/goal10#targets-and-indicators",
        "last_verified_date": "2026-10-24"
    },
    {
        "target_id": "11.6",
        "sdg_number": 11,
        "official_target_text": "By 2030, reduce the adverse per capita environmental impact of cities, including by paying special attention to air quality and municipal and other waste management.",
        "target_short_label": "Reduce Urban Environmental Impact",
        "source_url": "https://sdgs.un.org/goals/goal11#targets-and-indicators",
        "last_verified_date": "2026-10-24"
    },
    {
        "target_id": "12.6",
        "sdg_number": 12,
        "official_target_text": "Encourage companies, especially large and transnational companies, to adopt sustainable practices and to integrate sustainability information into their reporting cycle.",
        "target_short_label": "Adopt Corporate Sustainability Reporting",
        "source_url": "https://sdgs.un.org/goals/goal12#targets-and-indicators",
        "last_verified_date": "2026-10-24"
    },
    {
        "target_id": "13.2",
        "sdg_number": 13,
        "official_target_text": "Integrate climate change measures into national policies, strategies and planning.",
        "target_short_label": "Integrate Climate Measures into Policies",
        "source_url": "https://sdgs.un.org/goals/goal13#targets-and-indicators",
        "last_verified_date": "2026-10-24"
    },
    {
        "target_id": "13.3",
        "sdg_number": 13,
        "official_target_text": "Improve education, awareness-raising and human and institutional capacity on climate change mitigation, adaptation, impact reduction and early warning.",
        "target_short_label": "Build Climate Institutional Capacity",
        "source_url": "https://sdgs.un.org/goals/goal13#targets-and-indicators",
        "last_verified_date": "2026-10-24"
    },
    {
        "target_id": "16.6",
        "sdg_number": 16,
        "official_target_text": "Develop effective, accountable and transparent institutions at all levels.",
        "target_short_label": "Effective & Transparent Institutions",
        "source_url": "https://sdgs.un.org/goals/goal16#targets-and-indicators",
        "last_verified_date": "2026-10-24"
    },
    {
        "target_id": "16.10",
        "sdg_number": 16,
        "official_target_text": "Ensure public access to information and protect fundamental freedoms, in accordance with national legislation and international agreements.",
        "target_short_label": "Public Access to Information & Privacy",
        "source_url": "https://sdgs.un.org/goals/goal16#targets-and-indicators",
        "last_verified_date": "2026-10-24"
    },
    {
        "target_id": "17.16",
        "sdg_number": 17,
        "official_target_text": "Enhance the Global Partnership for Sustainable Development, complemented by multi-stakeholder partnerships that mobilize and share knowledge, expertise, technology and financial resources...",
        "target_short_label": "Multi-Stakeholder Partnerships",
        "source_url": "https://sdgs.un.org/goals/goal17#targets-and-indicators",
        "last_verified_date": "2026-10-24"
    },
    {
        "target_id": "17.18",
        "sdg_number": 17,
        "official_target_text": "By 2020, enhance capacity-building support to developing countries, including for least developed countries and small island developing States, to increase significantly the availability of high-quality, timely and reliable data...",
        "target_short_label": "High-Quality & Reliable Data Capacity",
        "source_url": "https://sdgs.un.org/goals/goal17#targets-and-indicators",
        "last_verified_date": "2026-10-24"
    }
]

def build_references():
    goals_path = os.path.join(SDG_DIR, "sdg_goals_v1.json")
    with open(goals_path, "w", encoding="utf-8") as f:
        json.dump({
            "version": "1.0.0",
            "module": "M5_SDG_IMPACT_MAPPING_ENGINE",
            "reference_standard": "United Nations 2030 Agenda for Sustainable Development",
            "total_goals": len(SDG_GOALS),
            "generated_date": "2026-10-24",
            "goals": SDG_GOALS
        }, f, indent=2)
    print(f"Saved {len(SDG_GOALS)} SDG goals to {goals_path}")

    targets_path = os.path.join(SDG_DIR, "sdg_targets_v1.json")
    with open(targets_path, "w", encoding="utf-8") as f:
        json.dump({
            "version": "1.0.0",
            "module": "M5_SDG_IMPACT_MAPPING_ENGINE",
            "reference_standard": "United Nations Global Indicator Framework for the SDGs",
            "total_targets": len(SDG_TARGETS),
            "generated_date": "2026-10-24",
            "targets": SDG_TARGETS
        }, f, indent=2)
    print(f"Saved {len(SDG_TARGETS)} SDG targets to {targets_path}")

if __name__ == "__main__":
    build_references()
