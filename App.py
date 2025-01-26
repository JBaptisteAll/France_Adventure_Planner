import streamlit as st

# PAGES
Welcome_page = st.Page(
    page="pages/1_Welcome.py",
    title="France Adventure Planner",
    icon="🌤️",    
    default=True,
)

Mountains_page = st.Page(
    page="pages/2_Mountains.py",
    title="Trek & Mountains",
    icon="⛰️",
)

Sea_page = st.Page(
    page="pages/3_Sea_&_Sun.py",
    title="Sea & Sun",
    icon="🏖️",
)

Inspiration_page = st.Page(
    page="pages/4_Inspiration.py",
    title="Inspiration",
    icon="💡",
)

about_page = st.Page(
    page="pages/5_About_Me.py",
    title="About Me",
    icon="📝",
)

#NAVIGATION
pg = st.navigation(
    {
        "Project": [Welcome_page, Mountains_page, Sea_page, Inspiration_page],
        "Info": [about_page]
    }
)

#LOGO
st.logo("Assets/CouldBe.png")


pg.run()