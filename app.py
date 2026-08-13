from flask import Flask, request, jsonify, render_template, send_from_directory
import json
import os

app = Flask(__name__)

# ============ CORS ============
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

# ============ LOAD COLLEGE DATA ============
COLLEGE_DATA_PATH = "static/college_data.json"
college_data = {}

try:
    if os.path.exists(COLLEGE_DATA_PATH):
        with open(COLLEGE_DATA_PATH, "r", encoding="utf-8") as f:
            college_data = json.load(f)
        print("✅ college_data.json loaded!")
    else:
        print(f"❌ File not found: {COLLEGE_DATA_PATH}")
except Exception as e:
    print(f"❌ Error: {e}")

# ============ SMART CHATBOT ENGINE ============

def find_best_reply(message):
    m = message.lower().strip()
    
    # ===== GREETINGS =====
    if any(word in m for word in ['hi', 'hello', 'hey', 'vanakkam', 'namaste', 'good morning', 'good evening']):
        return """👋 <b>Vanakkam!</b> Welcome to Mahendra Engineering College!<br><br>
I'm <b>Campus Compass</b>, your MEC buddy. Ask me about:<br>
• 👨‍🏫 <b>HODs & Faculty</b> (e.g., "Who is AIDS HOD?")<br>
• 📍 <b>Locations</b> (e.g., "Where is AI & DS lab?")<br>
• 🚌 <b>Bus & Transport</b><br>
• 🏠 <b>Hostel & Canteen</b><br>
• 💼 <b>Placements</b><br>
• 🧭 <b>Navigate to campus</b>"""

    # ===== WHO ARE YOU =====
    if any(word in m for word in ['who are you', 'what is your name', 'your name']):
        return "🎓 I'm <b>Campus Compass AI</b>, your virtual assistant for <b>Mahendra Engineering College</b>, Mallasamudram!"

    # ===== NAVIGATION =====
    if any(word in m for word in ['navigate', 'direction', 'how to reach', 'how to come', 'route', 'map']):
        return """🧭 <b>Navigate to MEC</b><br><br>
📍 <b>Address:</b> Salem-Tiruchengode Highway, Mahendhirapuri, Mallasamudram West, Namakkal - 637503<br><br>
🗺️ Use the <b>From → To</b> dropdowns on the map to navigate between buildings!<br><br>
🚂 <b>Nearest Railway:</b> Magudanchavadi (13.8 km)<br>
✈️ <b>Nearest Airport:</b> Salem (46.1 km)"""

    # ===== DISTANCE =====
    if any(word in m for word in ['how far', 'distance', 'where am i', 'my location']):
        return """📍 Click the <b>"Me"</b> button on the map to detect your current location and see distance from MEC!"""

    # ===== DEPARTMENT DETECTION =====
    depts = college_data.get("departments", {})
    
    dept_key = None
    dept_keywords = {
        'cse': ['cse', 'computer science', 'computer', 'cs'],
        'it': ['it', 'information technology', 'information tech'],
        'ece': ['ece', 'electronics and communication', 'electronics'],
        'eee': ['eee', 'electrical and electronics', 'electrical'],
        'mech': ['mech', 'mechanical', 'mechanical engineering'],
        'civil': ['civil', 'civil engineering'],
        'auto': ['auto', 'automobile', 'automotive'],
        'biomedical': ['biomedical', 'bme', 'bio medical'],
        'aids': ['aids', 'ai & ds', 'ai and ds', 'artificial intelligence and data science', 
                 'artificial intelligence', 'data science', 'ai', 'machine learning', 
                 'deep learning', 'dr. ananth', 'ananth'],
        'aeronautical': ['aeronautical', 'aerospace', 'aero'],
        'agricultural': ['agricultural', 'agri'],
        'english': ['english', 'english dept'],
        'chemistry': ['chemistry', 'chem'],
        'mathematics': ['mathematics', 'maths', 'math']
    }
    
    for key, keywords in dept_keywords.items():
        if any(k in m for k in keywords):
            dept_key = key
            break
    
    # AIDS SPECIFIC
    if any(x in m for x in ['aids hod', 'ai hod', 'data science hod', 'ananth', 'who is aids hod']):
        aids = depts.get("aids", {})
        return f"""🧠 <b>AI & Data Science HOD</b><br><br>
👨‍🏫 <b>{aids.get('hod', 'Dr. S. Ananth')}</b><br>
📍 <b>Block:</b> {aids.get('block', 'Academic Block A')}<br>
📞 <b>Phone:</b> {aids.get('phone', '(0427) 2482884')}<br>
👥 <b>Faculty:</b> {aids.get('faculty_count', '15')} members"""

    # GENERAL DEPT QUERIES
    if dept_key and dept_key in depts:
        dept = depts[dept_key]
        
        if any(word in m for word in ['hod', 'head', 'who is the head']):
            return f"""👨‍🏫 <b>{dept.get('name', dept_key.upper())} HOD</b><br><br>
🎓 <b>{dept.get('hod', 'N/A')}</b><br>
📍 <b>Block:</b> {dept.get('block', 'N/A')}<br>
🏢 <b>Floor:</b> {dept.get('floor', 'N/A')}"""
        
        if any(word in m for word in ['faculty', 'staff', 'professor', 'teacher']):
            faculty_list = dept.get('faculty', [])
            hod = dept.get('hod', '')
            name = dept.get('name', dept_key.upper())
            if faculty_list:
                formatted = "<br>".join([f"• {f}" for f in faculty_list[:10]])
                if len(faculty_list) > 10:
                    formatted += f"<br><i>...and {len(faculty_list) - 10} more</i>"
                return f"""👨‍🏫 <b>{name} Faculty</b><br><br>
<b>HOD:</b> {hod}<br><br><b>Faculty:</b><br>{formatted}"""
            else:
                return f"""👨‍🏫 <b>{name}</b><br><br>🎓 <b>HOD:</b> {hod}<br>👥 <b>Total:</b> {dept.get('faculty_count', 'N/A')}"""
        
        if any(word in m for word in ['course', 'degree', 'be', 'b.tech', 'study']):
            courses = dept.get('courses', [])
            return f"""📚 <b>{dept.get('name', dept_key.upper())} Courses</b><br><br>{'<br>'.join([f'• {c}' for c in courses])}"""
        
        if any(word in m for word in ['lab', 'laboratory', 'workshop']):
            labs = dept.get('labs', []) or dept.get('workshops', [])
            if labs:
                return f"""🔬 <b>{dept.get('name', dept_key.upper())} Labs</b><br><br>{'<br>'.join([f'• {l}' for l in labs])}"""
        
        return f"""🏛️ <b>{dept.get('name', dept_key.upper())}</b><br><br>
👨‍🏫 <b>HOD:</b> {dept.get('hod', 'N/A')}<br>
📍 <b>Block:</b> {dept.get('block', 'N/A')}<br>
🏢 <b>Floor:</b> {dept.get('floor', 'N/A')}"""

    # ALL HODS
    if 'hod' in m or 'head of department' in m:
        reply = "👨‍🏫 <b>HODs of All Departments</b><br><br>"
        for key, dept in depts.items():
            reply += f"• <b>{dept.get('name', key.upper())}:</b> {dept.get('hod', 'N/A')}<br>"
        return reply

    # ALL FACULTY
    if 'all faculty' in m or 'all staff' in m or 'all teachers' in m:
        reply = "👨‍🏫 <b>All Department HODs</b><br><br>"
        for key, dept in depts.items():
            reply += f"• <b>{dept.get('name', key.upper())}:</b> {dept.get('hod', 'N/A')}<br>"
        return reply

    # LIBRARY
    if 'library' in m:
        lib = college_data.get("library", {})
        return f"""📚 <b>{lib.get('name', 'Central Library')}</b><br><br>
🕐 <b>Timings:</b> {lib.get('timings', '8 AM - 8 PM')}<br>
📍 <b>Location:</b> {lib.get('location', 'Near Main Block')}<br>
🏢 <b>Floor:</b> {lib.get('floor', 'Ground + 1st')}<br>
📖 <b>Books:</b> {lib.get('books', '50,000+')}"""

    # CANTEEN
    if any(word in m for word in ['canteen', 'food', 'lunch', 'breakfast', 'snack', 'mess']):
        cant = college_data.get("canteen", {})
        timings = cant.get('timings', {})
        return f"""🍕 <b>{cant.get('name', 'College Canteen')}</b><br><br>
📍 <b>Location:</b> {cant.get('location', 'Near Hostel Block')}<br>
🍳 <b>Breakfast:</b> {timings.get('breakfast', '7:30 - 9:30 AM')}<br>
🍛 <b>Lunch:</b> {timings.get('lunch', '12 - 3 PM')}<br>
🍪 <b>Snacks:</b> {timings.get('snacks', '4 - 6 PM')}<br>
🥗 <b>Type:</b> {cant.get('type', 'Veg & Non-Veg')}"""

    # HOSTEL
    if 'hostel' in m or 'accommodation' in m or 'stay' in m:
        hostel = college_data.get("hostel", {})
        boys = hostel.get('boys', {})
        girls = hostel.get('girls', {})
        return f"""🏠 <b>Hostel Facilities</b><br><br>
👦 <b>Boys Hostel:</b> {boys.get('location', 'East Campus')}<br>
👧 <b>Girls Hostel:</b> {girls.get('location', 'West Campus')}<br>
💰 <b>Rent:</b> ~{boys.get('rent', '₹50,000/year')}<br><br>
📶 Wi-Fi | 🔒 24/7 Security | 🚿 Hot Water<br>
🏋️ Gym | 🎮 Indoor Games | 📖 Reading Room"""

    # BUS
    if any(word in m for word in ['bus', 'transport', 'college bus', 'route']):
        tr = college_data.get("transport", {})
        return f"""🚌 <b>College Transport</b><br><br>
🕐 <b>Timings:</b> {tr.get('timings', '7:30 AM - 6:30 PM')}<br>
🚏 <b>Bus Stop:</b> {tr.get('bus_stop', 'Main Entrance')}<br><br>
🛣️ <b>Routes:</b><br>{'<br>'.join([f'• {r}' for r in tr.get('bus_routes', [])])}"""

    # PLACEMENTS
    if any(word in m for word in ['placement', 'company', 'job', 'recruiter', 'salary', 'package']):
        pl = college_data.get("placements", {})
        stats = pl.get("2024_stats", {})
        return f"""💼 <b>Training & Placement Cell</b><br><br>
📊 <b>2024 Stats:</b><br>
✅ <b>Placed:</b> {stats.get('placed', '920')} students<br>
💰 <b>Median Salary:</b> {stats.get('median_salary', '₹4.0 LPA')}<br><br>
🏢 <b>Top Recruiters:</b><br>{', '.join(stats.get('top_recruiters', [])[:6])}"""

    # CONTACT
    if any(word in m for word in ['contact', 'phone', 'mobile', 'email', 'call', 'address']):
        c = college_data.get("contact", {})
        loc = college_data.get("location", "")
        return f"""📞 <b>Contact MEC</b><br><br>
☎️ <b>Phone:</b> {c.get('phone', '')}<br>
📱 <b>Mobile:</b> {c.get('mobile', '')}<br>
📧 <b>Email:</b> {c.get('email', '')}<br>
🌐 <b>Website:</b> {c.get('website', 'www.mahendra.info')}<br><br>
📍 <b>Address:</b><br>{loc}"""

    # ACHIEVEMENTS
    if any(word in m for word in ['achievement', 'ranking', 'naac', 'award', 'star']):
        ach = college_data.get("achievements", {})
        return f"""🏆 <b>MEC Achievements</b><br><br>
⭐ <b>NAAC:</b> {ach.get('naac', 'A Grade')}<br>
🌟 <b>MHRD-AICTE IIC:</b> {ach.get('iic_rating', '4-Star')}<br>
📈 <b>ARIIA 2021:</b> {ach.get('ariia_2021', 'Band EXCELLENT')}<br>
📄 <b>Publications:</b> {ach.get('publications', '131+')}<br>
🔬 <b>Patents:</b> {ach.get('patents', '14')}<br>
💰 <b>Research Grants:</b> {ach.get('research_grants', '₹57 Lakhs')}"""

    # PRINCIPAL
    if 'principal' in m:
        p = college_data.get("principal", "Dr. T. Elango")
        return f"""🎓 <b>Principal</b><br><br>👨‍🏫 <b>{p}</b><br><br>🏆 Innovation & Sustainability Award (IEI Salem, 2022)"""

    # MANAGEMENT
    if any(word in m for word in ['management', 'chairman', 'founder', 'trust', 'director']):
        return f"""🏛️ <b>Mahendra Educational Trust</b><br><br>
👤 <b>Founder:</b> {college_data.get('trust_founder', 'Shri. M.G. Bharath Kumar')}<br>
👔 <b>Chairman:</b> {college_data.get('chairman', 'Thiru M.G. Bharath Kumar')}<br>
👩 <b>Secretary:</b> {college_data.get('secretary', 'Tmt. Valliyammal Bharath Kumar')}<br>
👨‍💼 <b>MD:</b> {college_data.get('managing_director', 'Thiru Ba. Mahendhiran')}"""

    # SPORTS
    if any(word in m for word in ['sport', 'game', 'gym', 'cricket', 'football']):
        sp = college_data.get("sports", {})
        return f"""⚽ <b>Sports Facilities</b><br><br>
🏠 <b>Indoor:</b> {', '.join(sp.get('indoor', []))}<br>
🌳 <b>Outdoor:</b> {', '.join(sp.get('outdoor', []))}<br>
🏋️ <b>Gym:</b> {sp.get('gym', 'Available in Hostel Block')}"""

    # FACILITIES
    if any(word in m for word in ['facility', 'wifi', 'internet', 'computer', 'atm']):
        fac = college_data.get("facilities", {})
        return f"""🏫 <b>Campus Facilities</b><br><br>
📶 <b>Wi-Fi:</b> {fac.get('wifi', 'Campus-wide')}<br>
💻 <b>Computers:</b> {fac.get('computers', '600+ systems')}<br>
🏧 <b>ATM:</b> {fac.get('atm', 'Near Main Gate')}<br>
🏥 <b>Medical:</b> {fac.get('medical', 'First Aid Center')}<br>
🅿️ <b>Parking:</b> {fac.get('parking', 'Available')}"""

    # RESEARCH
    if any(word in m for word in ['research', 'phd', 'supervisor', 'publication']):
        sups = college_data.get("research_supervisors", [])
        reply = "🔬 <b>Research Supervisors (Anna University)</b><br><br>"
        for s in sups[:7]:
            reply += f"• <b>{s.get('name')}</b> - {s.get('dept', '')}<br>"
        return reply

    # WOMEN EMPOWERMENT
    if any(word in m for word in ['women', 'girl', 'ladies', 'empowerment']):
        we = college_data.get("women_empowerment_cell", {})
        return f"""👩 <b>Women Empowerment Cell</b><br><br>
👩‍🏫 <b>Head:</b> {we.get('head', 'Dr. P. Jamunarani')}<br><br>
🎯 <b>Activities:</b><br>{'<br>'.join([f'• {a}' for a in we.get('activities', [])])}"""

    # NSS
    if 'nss' in m or 'social service' in m:
        nss = college_data.get("nss_activities", [])
        return f"""🌟 <b>NSS Activities</b><br><br>{'<br>'.join([f'• {a}' for a in nss[:8]])}"""

    # TIME
    if any(word in m for word in ['time', 'timing', 'when', 'hour', 'open', 'close']):
        return """🕐 <b>General Timings</b><br><br>
🏫 <b>College Hours:</b> 8:30 AM - 4:30 PM<br>
📚 <b>Library:</b> 8:00 AM - 8:00 PM<br>
🍕 <b>Canteen:</b> 7:30 AM - 6:00 PM<br>
🚌 <b>Bus:</b> 7:30 AM - 6:30 PM<br>
🏠 <b>Hostel:</b> 24/7 (Entry till 9 PM)"""

    # DEFAULT
    return """🤔 <b>Sorry, I don't have that information.</b><br><br>
Try asking me about:<br>
• 👨‍🏫 HODs & Faculty (e.g., "Who is AIDS HOD?")<br>
• 📍 Locations (e.g., "Where is the library?")<br>
• 🚌 Bus routes & timings<br>
• 🏠 Hostel & Canteen<br>
• 💼 Placements<br>
• 📞 Contact details<br><br>
Or tap a quick button below! 👇"""

# ============ ROUTES ============

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/logo")
def logo():
    return send_from_directory("static", "logo.png")

@app.route("/test")
def test():
    return jsonify({
        "status": "OK",
        "data_loaded": bool(college_data),
        "college_name": college_data.get("college_name", "NOT LOADED")
    })

@app.route("/chat", methods=["POST", "OPTIONS"])
def chat():
    if request.method == "OPTIONS":
        return jsonify({"status": "ok"})

    try:
        data = request.get_json()
        if not data or "message" not in data:
            return jsonify({"reply": "Please send a message!"}), 400

        message = data["message"]
        print(f"📩 User: {message}")

        reply = find_best_reply(message)
        print(f"✅ Reply: {reply[:50]}...")
        
        return jsonify({"reply": reply})

    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"reply": "Sorry, something went wrong!"}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)