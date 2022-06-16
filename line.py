import pandas as pd # Import Library Pandas
from bokeh.models.sources import ColumnDataSource # import struktur fundamental bokeh
from bokeh.models import Select, Panel # import fitur interaktif select dan panel
from bokeh.layouts import column, row  # import column dan row untuk layouting tampilan halaman website
from bokeh.plotting import figure # import figure untuk membuat plot

def Tab_LinePlot(frame):
    # Inisialisasi variabel List_Saham untuk menentukan pergerakan saham yang akan digunakan
    List_Saham = ["Alcatel.JK", "VIVO.JK", "apple.JK", "lenovo.JK", "lg.JK", "nokia.JK", "pixel.JK", "samsung.JK", "xiaomi.JK", "zte.JK"]
    
    # Inisialisasi variabel START dan END untuk menentukan pergerakan saham di awal dan akhir tahun 2020
    START, END = "2020-1-01", "2020-12-31"

    # Inisialisasi function load_Saham digunakan untuk mengambil data dari yfinance
    def load_Saham(Saham):
        df = frame.download(Saham, start=START, end=END) # Download dataset dari yfinance dan disimpan dalam dataframe df
        return df["Close"].dropna() # Melakukan drop missing value kolom "Close"

    # Inisialisasi function get_data dengan mengakses var s1, s2
    def get_data(s1, s2):
        d = load_Saham(List_Saham) 
        df = d[[s1, s2]] 
        returns = df.pct_change().add_suffix("_returns")
        df = pd.concat([df, returns], axis=1)
        df.rename(columns={s1:"s1", s2:"s2", s1+"_returns":"s1_returns", s2+"_returns":"s2_returns"}, inplace=True)
        return df.dropna()

    # Inisialisasi function saham yang mengembalikan list daftar saham 
    def saham(val, lst): 
        return [x for x in lst if x!= val]
    saham1 = Select(value="Alcatel.JK", options = saham("VIVO.JK", List_Saham)) # saham1 menyimpan selection saham berdasarkan List_Saham
    saham2 = Select(value="VIVO.JK", options = saham("Alcatel.JK", List_Saham)) # saham2 menyimpan selection saham berdasarkan List_Saham

    # Source data
    data = get_data(saham1.value, saham2.value )
    source =  ColumnDataSource(data=data)

    # Set tools yang akan digunakna pada Plots
    tools = "pan, wheel_zoom, xbox_select, reset"
    
    # Membuat grafik pergerakan saham pilihan kesatu
    graf1 = figure(width = 700, height = 250, tools=tools, x_axis_type="datetime", active_drag="xbox_select")
    graf1.line("Date", "s1", source=source)
    graf1.circle("Date", "s1", size=1, source=source, color=None, selection_color="firebrick")

    # Membuat grafik pergerakan saham pilihan kedua
    graf2 = figure(width = 700, height = 250, tools=tools, x_axis_type="datetime", active_drag="xbox_select")
    graf2.x_range = graf1.x_range
    graf2.line("Date", "s2", source=source)
    graf2.circle("Date", "s2", size=1, source=source, color=None, selection_color="firebrick")

    # Callbacks
    # Inisialisasi function saham1_change untuk melakukan update grafik sesuai saham yang dipilih
    def saham1_change(attrname, old, new):
        saham2.options = saham(new, List_Saham)
        update()

    # Inisialisasi function saham2_change untuk melakukan update grafik sesuai saham yang dipilih
    def saham2_change(attrname, old, new):
        saham1.options = saham(new, List_Saham)
        update()

    # Inisialisasi function update melakukan update grafik 
    def update():
        s1, s2 = saham1.value, saham2.value
        df = get_data(s1,s2)
        source.data = df
        graf1.title.text, graf2.title.text = s1,s2

    # Melakukan update saham yang dipilih  
    saham1.on_change("value", saham1_change)
    saham2.on_change("value", saham2_change) 

    # Set layout tampilan pada halaman website
    widgets = column(saham1, saham2)
    series = column(graf1, graf2)
    main_row = row(widgets, series)

    # Membuat tab dengan layout
    tab = Panel(child=main_row, title = "Line Plot")
    return tab