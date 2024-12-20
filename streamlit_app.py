import streamlit
import pandas
import plotly.express as px
import plotly.graph_objects as go

streamlit.set_page_config(
    page_title = "Séance 6 | Demande | Correction",
    page_icon = ":student:",
    layout = "wide"
)

streamlit.title("Séance 6 -- Demande -- Correction")

data = pandas.read_csv("scimagojr.csv")
temp2a = data.filter(["Region", "Year", "Documents"]).groupby(["Region", "Year"]).sum()
temp2b = temp2a.reset_index().pivot(index = "Year", columns = "Region", values = "Documents")
temp2c = temp2b.copy()
for v in temp2c:
    temp2c[v] = temp2c[v] / temp2c[v][1996]

temp2d = pandas.melt(temp2c.reset_index(), id_vars = ["Year"])
temp2e = temp2d

temp3 = data.query("Year == 2021")

col1, col2 = streamlit.columns(2)

with col1:
    # Graphique 1 : diagramme en barres de la production scientifique par régions du monde
    temp1 = data.filter(["Region", "Documents"]).groupby("Region").sum()
    fig1 = px.bar(
        temp1.reset_index().sort_values(by = "Documents"),
        y = "Region",
        x = "Documents"
    )
    streamlit.caption("Classement des régions selon la production scientifique")
    fig1.update_traces(marker_color = "darkred")
    selection = streamlit.plotly_chart(fig1, on_select = "rerun", selection_mode = "points")

if (selection["selection"]["points"]):
    region_selection = selection["selection"]["points"][0]["label"]
    temp2e["Région"] = [region_selection if r == region_selection else "Autres" for r in temp2d["Region"]]
    couleurs2 = ["lightgray", "darkred"]
    couleurs3 = couleurs2
    temp3["Couleur"] = [region_selection if r == region_selection else "Autres" for r in temp3["Region"]]
    taille3 = [5 if r == region_selection else 1 for r in temp3["Region"]]
else:
    temp2e["Région"] = temp2d["Region"]
    couleurs2 = px.colors.colorbrewer.Set1
    temp3["Couleur"] = "tous"
    couleurs3 = ["gray"]
    taille3 = [1 for r in temp3["Region"]]

with col2:
    fig2b = px.line(
        temp2e,
        x = "Year",
        y = "value",
        line_group = "Region",
        color = "Région",
        color_discrete_sequence = couleurs2
    )
    streamlit.caption("Evolution en base 100 entre 1996 et 2021")
    streamlit.plotly_chart(fig2b)


fig3 = px.scatter(
    temp3,
    x = "Documents",
    y = "Citations",
    color = "Couleur",
    size = taille3,
    color_discrete_sequence = couleurs3,
    log_x = True, log_y= True
)
fig3.update_layout(showlegend = False)
streamlit.caption("Croisement en documents produits et citations en 2021")
streamlit.plotly_chart(fig3)
