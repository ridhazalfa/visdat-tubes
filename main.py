import pandas as pd
import glob

from bokeh.models.widgets import Tabs # import Tabs digunakna untuk membuat tab halaman website
from bokeh.io import curdoc # import curdoc

# Memanggil fungsi Tab Korelasi dan Line 
from Tab_Corr import Tab_Corellation 
from Tab_Line import Tab_LinePlot 

path = r'./Saham Smartphone' # use your path
all_files = glob.glob(os.path.join(path , "/*.csv"))

li = []

for filename in all_files:
    df = pd.read_csv(filename, index_col=None, header=0)
    li.append(df)

frame = pd.concat(li, axis=0, ignore_index=True)

# Membuat Tab 
tab1 = Tab_Corellation(frame)
tab2 = Tab_LinePlot(frame)

# Masukkan semua tab ke dalam satu aplikasi
tabs = Tabs(tabs = [tab1, tab2])

# Put the tabs in the current document for display
curdoc().add_root(tabs)
curdoc().title = "Pergerakan Saham Smartphone di Indonesia"