import json
from textwrap import dedent

INSTRUCTION = dedent("""
<Instruction>
You are an advanced AI trained to label social media posts related to crisis situations, specifically natural disasters.
Your goal is to label the given posts and social media videos.

Hard rules:
Use visual evidence from attached video to classify the post.
Do not infer solely from title, description, transcript, hashtags, or prior knowledge.
If visual evidence is insufficient, explicitly return insufficient_visual_evidence.
Adhere to output formats strictly, ensuring all required fields are present in correctly formatted JSON.

</Instruction>
""").strip()

TAXONOMY = {
    "Supplies": [
        "Transport",
        "Medical",
        "Water, Sanitation, and Hygiene (WASH)",
        "Shelter and Housing",
        "Equipment and Tools",
        "Food and Nutrition",
        "Clothing and Warmth",
        "Communication and Power",
        "Education and Recreation",
        "Money",
        "Infant Care",
    ],
    "Emergency Personnel": [
        "Search and Rescue Teams",
        "Medical and Health Teams",
        "Fire and Hazard Control",
        "Law Enforcement and Security",
        "Logistics and Coordination Teams",
        "Communication and IT Teams",
        "Shelter and Housing Teams",
        "Community and Social Support Teams",
        "Energy and Infrastructure Repair Teams",
        "Recovery and Rehabilitation Teams",
        "Legal and Advocacy Teams",
    ],
    "Actions": [
        "Search and Rescue",
        "Medical Assistance",
        "Shelter and Housing Support",
        "Food and Water Distribution",
        "Infrastructure Repair and Debris Clearance",
        "Transportation Services",
        "Security and Crowd Control",
        "Information and Communication",
        "Resource Coordination and Supply Management",
        "Community and Social Support",
        "Recovery and Rehabilitation",
    ],
}
TAXONOMY_JSON = json.dumps(TAXONOMY, indent=2)

FULL_TAXONOMY = {
    "Taxonomy": {
      "Supplies": {
        "Transport": [
          "Spare Parts",
          "Vehicles"
        ],
        "Medical": [
          "Wound Care and First Aid Supplies",
          "Tools, Accessories, and Protective Gear",
          "Medications and Treatment Supplies",
          "Diagnostic",
          "Respiratory Equipment",
          "Mobility Aids",
          "Laboratory Equipment",
          "Cold Chain and Temperature-Controlled Storage"
        ],
        "Water, Sanitation, and Hygiene (WASH)": [
          "Water Storage",
          "Borehole Construction",
          "Pumps",
          "Water Distribution",
          "Water Testing",
          "Water Treatment",
          "Sanitation Facilities",
          "Personal Hygiene",
          "Cleaning Supplies"
        ],
        "Shelter and Housing": [
          "Shelter",
          "Covers and Linings",
          "Accessories"
        ],
        "Equipment and Tools": [
          "IT and Office Supplies",
          "Emergency Tools",
          "Basic Tools",
          "Material Handling Equipment",
          "Kitchen Items"
        ],
        "Food and Nutrition": [
          "Staples",
          "Proteins",
          "Cooking Essentials",
          "High-Energy Foods",
          "Ready-to-Eat Foods",
          "Beverages",
          "Other Essentials"
        ],
        "Clothing and Warmth": [
          "Clothing",
          "Warmth Items",
          "Other Clothing"
        ],
        "Communication and Power": [
          "Communication Tools",
          "Power Supply",
          "Lighting"
        ],
        "Education and Recreation": [
          "Educational Supplies",
          "Recreational Items"
        ],
        "Money": [
        ],
        "Infant Care": [
          "Comfort Packs for Children",
          "Pacifiers",
          "Baby Carriers",
          "Trolleys"
        ]
      },
      "Emergency Personnel": {
        "Search and Rescue Teams": [
          "Urban Search and Rescue (USAR) teams",
          "Water Rescue Teams",
          "K9 Search Teams",
          "Mountain/High Angle Rescue",
          "Specialized Medical Rescuers"
        ],
        "Medical and Health Teams": [
          "Emergency Medical Technicians (EMTs)",
          "Paramedics",
          "Doctors",
          "Surgeons",
          "Psychosocial Support Teams",
          "Mental Health Professionals",
          "Infection Control Experts",
          "Public Health Teams"
        ],
        "Fire and Hazard Control": [
          "Firefighting Teams",
          "Hazardous Materials (HAZMAT) Teams",
          "Fire Safety Inspectors"
        ],
        "Law Enforcement and Security": [
          "Police Officers",
          "Military Police",
          "Community Liaison Officers",
          "Forensic Teams",
          "Evacuation Personnel"
        ],
        "Logistics and Coordination Teams": [
          "Disaster Coordination Officers",
          "Relief Operations Coordinators",
          "Transport and Supply Chain Teams",
          "Volunteers"
        ],
        "Communication and IT Teams": [
          "Emergency Communications Specialists",
          "Satellite Communications Technicians",
          "Public Information Officers",
          "Media Liaison Officers",
          "ICT Specialists"
        ],
        "Shelter and Housing Teams": [
          "Shelter Managers",
          "Emergency Housing Specialists",
          "Construction Teams"
        ],
        "Community and Social Support Teams": [
          "Child Protection Teams",
          "Gender-Based Violence (GBV) Specialists",
          "Elderly Care Specialists",
          "Community Outreach Workers"
        ],
        "Energy and Infrastructure Repair Teams": [
          "Electricians",
          "Water and Sanitation Technicians",
          "Road Construction Crews"
        ],
        "Recovery and Rehabilitation Teams": [
          "Reconstruction Teams",
          "Economic Recovery Teams",
          "Education Support Teams"
        ],
        "Legal and Advocacy Teams": [
          "Legal Aid Teams",
          "Advocacy Teams"
        ]
      },
      "Actions": {
        "Search and Rescue": [
          "Search for Missing Persons",
          "Evacuation Support",
          "Water Rescue"
        ],
        "Medical Assistance": [
          "First Aid and Triage",
          "Hospitalization and Treatment",
          "Psychosocial and Mental Health"
        ],
        "Shelter and Housing Support": [
          "Setting Up Temporary Shelters",
          "Repair and Retrofitting"
        ],
        "Food and Water Distribution": [
          "Food Aid",
          "Water Supply"
        ],
        "Infrastructure Repair and Debris Clearance": [
          "Road and Bridge Clearing",
          "Utility Restoration",
          "Debris Removal"
        ],
        "Transportation Services": [
          "Evacuation Transport",
          "Ambulance and Medical Transport",
          "Supply and Personnel Transport"
        ],
        "Security and Crowd Control": [
          "Patrol and Perimeter Security",
          "Traffic and Crowd Management",
          "Incident Control Points"
        ],
        "Information and Communication": [
          "Public Announcements and Alerts",
          "Misinformation Management",
          "Hotline or Helpline Operation",
          "Translation and Interpretation Services"
        ],
        "Resource Coordination and Supply Management": [
          "Warehouse and Inventory Control",
          "Last-Mile Distribution",
          "Volunteer and Donations Management"
        ],
        "Community and Social Support": [
          "Child-Friendly Spaces",
          "Gender-Based Violence (GBV) Response",
          "Elderly and Special Needs Support",
          "Family Reunification"
        ],
        "Recovery and Rehabilitation": [
          "Livelihood Recovery",
          "Education Continuity",
          "Community Rehabilitation"
        ]
      }
    }
  }

FULL_TAXONOMY_JSON = json.dumps(FULL_TAXONOMY, indent=2)

CONTEXT = dedent(f"""
<Context>
Natural disasters, such as hurricanes, wildfires, earthquakes, floods, tornadoes, landslides, etc. have significant impacts on communities.

Each social media post of type Offer or Request can be represented as a triplet of themes: supplies, personnel, actions.

<Taxonomy>
{TAXONOMY_JSON}
</Taxonomy>

this is a more detailed version of the taxonomy to understand the components of the classes, do not use these as the target labels, but as a way to understand the taxonomy:

<Full Taxonomy>
{FULL_TAXONOMY_JSON}
</Full Taxonomy>

The social media data should be categorized into its specific type (Request, Offer, Other) and should be labeled based on supplies, action, emergency personnel.
</Context>
""").strip()

OUTPUT_FORMATS = dedent("""
<Output formats>
this is the output format when the type is either Request or Offer or both:
{
  "text": "The social media post text here",
  "type": ["Request"],
  "action_request": [],
  "personnel_request": [],
  "supplies_request": [],
  "action_offer": [],
  "personnel_offer": [],
  "supplies_offer": [],
  "actionability": false,
  "explanation": "...",
  "visual_evidence": "...",
  "confidence": 0.0 to 1.0,
  "insufficient_visual_evidence": true or false
}

this is the output format when the type is Other:
{
  "text": "The social media post text here",
  "type": ["Other"],
  "explanation": "..."
  "visual_evidence": "...",
  "confidence": 0.0 to 1.0,
  "insufficient_visual_evidence": true or false
}

</Output formats>
""").strip()

AMBIGUOUS_CLASSES = dedent("""
<ambiguous classes>
Supplies:
- Transport: Label posts as "transport" when they mention specific transport-related supplies or items associated with transportation vehicles.
- Equipment and Tools: Apply this label when posts involve the request or donation of tools and equipment.
- Shelter and Housing: This label applies to posts referencing places where people can stay or live.

Actions:
- Resource Coordination and Supply Management: Use this label for posts focused on the distribution, management, collection, or organization of supplies and resources.
- Information and Communication: Apply this label to posts that involve requesting advice or information, as well as those offering critical information.
- Recovery and Rehabilitation: Use this label for posts concerning actions after a disaster, focused on returning to normal life.
- Search and Rescue: Label posts as "Search and Rescue" if they involve requests for or offers of assistance in locating missing individuals or rescuing people.
- Community and Social Support: Use this label for posts that focus on providing support to vulnerable populations.

Emergency Personnel:
- Logistics and Coordination Teams: Teams or volunteers responsible for distributing supplies or managing logistics.
- Recovery and Rehabilitation Teams: Groups focused on medium- and long-term recovery.
- Shelter and Housing Teams: Teams who assist in setting up, repairing, or providing shelters and housing.
- Legal and Advocacy Teams: Individuals, professionals, or volunteers offering assistance with legal matters.
</ambiguous classes>
""").strip()

STOCK_EXAMPLES = dedent("""
{
  "text": "If anyone knows how to contact ppl in Aab Barik, plz DM. Worried sick. #AfghanLandslides",
  "type": ["Request"],
  "action_request": ["Information and Communication"],
  "personnel_request": [],
  "supplies_request": [],
  "action_offer": [],
  "personnel_offer": [],
  "supplies_offer": [],
  "actionability": false,
  "explanation": "Seeking personal contact info; not an urgent supply or rescue request."
}

{
  "text": "Does anyone know how to access the wildfire relief fund? The site keeps crashing. #CaliforniaFires",
  "type": ["Request"],
  "action_request": ["Information and Communication"],
  "personnel_request": [],
  "supplies_request": [],
  "action_offer": [],
  "personnel_offer": [],
  "supplies_offer": [],
  "actionability": false,
  "explanation": "Asking for instructions on relief fund site; no urgency or location."
}
""").strip()


def build_prompt(post_title: str, post_desc: str, additional_examples: str = "") -> str:
    post_text = f"{post_title}\n{post_desc}"
    return dedent(f"""
{INSTRUCTION}

{CONTEXT}

{OUTPUT_FORMATS}

{AMBIGUOUS_CLASSES}

<Examples>
These are few examples of the classification:
{STOCK_EXAMPLES}
{additional_examples}
</Examples>

<Task>
Your task is to label the following social media post based on the taxonomy and rules mentioned above.
Only output the json dictionary and nothing else.
Take into account the ambiguous classes.
</Task>

social media title and description: {post_text}
social media video attached as frames.
""").strip()
