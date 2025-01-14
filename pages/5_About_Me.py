import streamlit as st

from forms.contact import contact_form

@st.dialog("Contact Me")
def show_contact_form():
    contact_form()

# Création de colonnes
col1, col2 = st.columns(2, gap="small", vertical_alignment="center")

# Colonne de gauche
with col1:
    st.image("Assets/JB_2.png", width=300)
    

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
Hi, I'm Jean-Baptiste! I'm a passionate learner currently diving deep into the world of data analysis and programming. 
After discovering my love for technology, I decided to embark on this journey to master Python, data analysis, and more.
In my free time, I love exploring nature, especially hiking in the mountains. 🏔️
""")

#st.write("#")
st.write("---")
# Section : Mon Parcours
st.markdown("# My Journey")

# Formation
st.markdown("### Education & Training")
st.markdown("""
My journey into data began as a self-taught learner. I explored various online platforms, including Coursera, 
where I completed courses offered by Google and Meta to build my foundational knowledge in data analytics. 📚

To validate my skills and take my expertise to the next level, I enrolled in a bootcamp with [Jedha](https://www.jedha.co/). 
This rigorous program provided me with hands-on experience in Python programming, data visualization, 
and machine learning, solidifying my capabilities as a future Data Analyst.
""")

# Compétences Acquises
st.markdown("### Skills Developed")
st.markdown("""
- **Programming**: Proficient in **SQL** and **Python**, with experience in libraries like Pandas, Matplotlib, and plotly.
- **Data Analysis**: Expertise in cleaning, exploring, and visualizing data to uncover actionable insights.
- **Visualization**: Strong hands-on experience and knowledge in **PowerBI** and **Tableau**.
- **Soft Skills**: Problem-solving, collaboration, and communication skills developed through projects and teamwork.
""")

# Projets Réalisés
st.markdown("### Key Projects")
st.markdown("""
- [**France Adventure Planner**](https://github.com/JBaptisteAll/France_Adventure_Planner): An application that combines weather data and user preferences to recommend the best travel destinations. Built with Python, Streamlit, and Plotly.
- [**Behind The Stream**](https://github.com/JBaptisteAll/Behind_the_Stream): Explored and visualized trends in Netflix's catalog using Power BI to uncover insights about user preferences and content availability.
""")
#- **Student Success Prediction**: Predicted students' final grades using machine learning models, demonstrating the impact of various factors on academic performance.

# Objectifs
st.markdown("### Goals & Aspirations")
st.markdown("""
My ultimate goal is to become a skilled data professional who can tackle complex challenges using data-driven approaches. 
I aspire to work on impactful projects, continue learning advanced techniques, 
and contribute to the tech community by sharing knowledge and building innovative solutions. 
""")

st.write("---")
# Section : Objectifs Futurs
st.markdown("## Future Plans")
st.markdown("""
- Enhance this application by adding more features, such as Snow Section or real-time updates.
- Continue developing my skills in data analysis and visualization.
- Contribute to open-source projects and build a strong portfolio for my dream job in the tech industry. 
""")
