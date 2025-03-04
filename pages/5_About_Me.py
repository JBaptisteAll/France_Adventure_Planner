import streamlit as st

from forms.contact import contact_form

@st.dialog("Contact Me")
def show_contact_form():
    contact_form()

# Création de colonnes
col1, col2 = st.columns(2, gap="small", vertical_alignment="center")

# Colonne de gauche
with col1:
    st.image("Assets/JB.jpg", width=300)
    

# Colonne de droite
with col2:
    st.markdown("""
        ### Contact me 📩""")
    
    if st.button("Contact Me"):
        show_contact_form()
    
    st.markdown("""
    [LinkedIn](https://www.linkedin.com/in/jean-baptiste-allombert/)  
    [GitHub](https://github.com/JBaptisteAll)
    """)
    #st.markdown("""Feel free to reach out to me.""")



st.write("#")
# Section : Présentation Personnelle
st.markdown("#### Welcome, Here's a little insight into who I am!")
st.markdown("## About Me")
st.markdown("""
Hi, I'm Jean-Baptiste! I'm a passionate learner currently diving deep into 
the world of data analysis and programming. After discovering my love for technology, 
I decided to embark on this journey to master Python, data analysis, and more.

With 20 years of experience in the hospitality and tourism industry, I have developed 
a deep understanding of sector challenges and provide tailored strategic analyses. 
Proficient in Python, SQL, Power BI, and Tableau, I identify trends, optimize 
decision-making, and enhance business performance.

In my free time, I love exploring nature, especially hiking in the mountains. 🏔️ 
Curious and self-driven, I seek to thrive in a dynamic environment where 
I can continue learning and delivering value.            
""")

#st.write("#")
st.write("---")
# Section : Mon Parcours
st.markdown("# My Journey")

# Formation
st.markdown("### Education & Training 🎓")
st.markdown("""
My journey into data began with a strong self-learning approach. 
Driven by curiosity and a passion for analytics, I explored various online 
platforms such as Coursera, where I successfully completed courses from 
Google and Meta, building a solid foundation in data analytics, Python programming, 
and SQL. 📊

To take my expertise to the next level and gain hands-on experience, 
I enrolled in an intensive Data Analytics Bootcamp at [Jedha](https://www.jedha.co/). 
Throughout this program, I worked on real-world datasets, developing skills in 
data manipulation, visualization, and machine learning. The bootcamp not only 
refined my technical abilities but also strengthened my problem-solving and 
analytical thinking through practical projects and teamwork.            
""")

# Compétences Acquises
st.markdown("### Skills Developed")
st.markdown("""
- **Programming**: Proficient in **SQL** and **Python**, with experience in libraries 
                like Pandas, Matplotlib, and plotly.
- **Data Analysis**: Expertise in cleaning, exploring, and visualizing data to 
                uncover actionable insights.
- **Visualization**: Strong hands-on experience and knowledge in **PowerBI** 
                and **Tableau**.
""")
st.markdown("""#### Soft Skills""")
st.markdown("""
- **Problem-Solving**: Ability to break down complex problems and 
                find efficient solutions.
- **Collaboration**: Experience working in team-based projects, 
                fostering a data-driven decision-making mindset.
- **Communication**: Strong presentation skills, translating 
                complex analytical findings into clear and actionable insights.
""")

# Projets Réalisés
st.markdown("### Key Projects")
st.markdown("""
- [**France Adventure Planner**](https://github.com/JBaptisteAll/France_Adventure_Planner): 
            Development of a Streamlit application (View the App) that allows users 
            to plan trips based on the weather, personal interests (sea or mountains), 
            with recommendations and links to hotels and trains.
            **Technologies**: Python (Pandas, Scrapy, Plotly), Make.com, GitHub Actions.

- [**Behind The Stream**](https://github.com/JBaptisteAll/Behind_the_Stream): 
            Creation of an interactive Power BI dashboard designed for 
            film industry professionals (production companies, distributors) 
            to analyze trends in Netflix’s catalog (genres, movies vs. series, 
            annual trends).
            **Technologies**: Excel, Power Query, Power BI.
""")
#- **Student Success Prediction**: Predicted students' final grades using machine learning models, demonstrating the impact of various factors on academic performance.

# Objectifs
st.markdown("### Goals & Aspirations")
st.markdown("""
My ultimate goal is to evolve into a highly skilled data professional, capable 
of tackling complex challenges using data-driven approaches. I am passionate about 
solving real-world problems with analytics, uncovering hidden patterns in data, 
and transforming insights into actionable strategies.

I aspire to work on impactful projects, particularly in areas where data can drive 
meaningful change, such as sustainability, smart cities, or AI-driven decision-making. 
Beyond mastering advanced analytical techniques, I also aim to contribute 
to the tech community, sharing knowledge, collaborating on open-source projects, 
and inspiring others on their own data journeys.
""")

st.write("---")
# Section : Objectifs Futurs
st.markdown("## Future Plans")
st.markdown("""
- **Enhancing this application** : I plan to expand this project by integrating 
                new features, such as real-time weather updates to provide users 
                with the most up-to-date forecasts.
- **Advancing my technical skills** : I continuously push myself to deepen my expertise 
                in data analysis, visualization, and machine learning, exploring 
                new tools and methodologies to stay at the forefront of the field.
- **Building a strong portfolio & contributing to open source** : I am committed to 
                developing a robust portfolio by working on diverse projects, 
                contributing to open-source initiatives, and actively engaging 
                with the data community to showcase my skills and expertise.
- **Landing my dream role in the tech industry** : Ultimately, my goal is to secure 
                a role in the tech industry where I can apply my knowledge to drive 
                innovation, optimize decision-making, and make a real impact.
""")
st.markdown("""
Every step I take in this journey is an opportunity to learn, grow, and create 
solutions that make a difference.
""")