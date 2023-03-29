import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def graphics(data,type,path,name_band,id,id_cross=None,num_columns=4,save=True,plot=True):
    '''Function to make graphs of the given data '''
    max=data[type].max()
    sns.set(rc={'figure.figsize':(15,12)})
    sns.set_theme(style="white")
    if id=='IC':
        col='Component'
    else:
        col='ROI'
    axs=sns.catplot(x='group',y=type,data=data,hue='database',dodge=True, kind="box",col=col,col_wrap=num_columns,palette='winter_r',fliersize=1.5,linewidth=0.5,legend=False)
    #plt.yticks(np.arange(0,round(max),0.1))
    axs.set(xlabel=None)
    axs.set(ylabel=None)
    if id_cross==None:
        axs.fig.suptitle(type+' in '+r'$\bf{'+name_band+r'}$'+ ' in the ICs of normalized data given by the databases')
    else:
        axs.fig.suptitle(type+' in '+id_cross+' of ' +r'$\bf{'+name_band+r'}$'+ ' in the ICs of normalized data given by the databases')
    if id=='IC':
        axs.add_legend(loc='upper right',bbox_to_anchor=(.59,.95),ncol=4,title="Database")
        axs.fig.subplots_adjust(top=0.85,bottom=0.121, right=0.986,left=0.05, hspace=0.138, wspace=0.062) 
        axs.fig.text(0.5, 0.04, 'Group', ha='center', va='center')
        axs.fig.text(0.01, 0.5,  type, ha='center', va='center',rotation='vertical')
    else:
        
        axs.add_legend(loc='upper right',bbox_to_anchor=(.7,.95),ncol=4,title="Database")
        axs.fig.subplots_adjust(top=0.85,bottom=0.121, right=0.986,left=0.06, hspace=0.138, wspace=0.062) # adjust the Figure in rp
        axs.fig.text(0.5, 0.04, 'Group', ha='center', va='center')
        axs.fig.text(0.015, 0.5,  type, ha='center', va='center',rotation='vertical')
    if plot:
        plt.show()
    if save==True:
        if id_cross==None:
            path_complete='{path}\Graficos_{type}\{id}\{name_band}_{type}_{id}.png'.format(path=path,name_band=name_band,id=id,type=type)  
        else:
            path_complete='{path}\Graficos_{type}\{id}\{name_band}_{id_cross}_{type}_{id}.png'.format(path=path,name_band=name_band,id=id,type=type,id_cross=id_cross)
        plt.savefig(path_complete)
    plt.close()
    return path_complete

def text_format(val,value):
    if value==0.2: #Cambie el 0.05 por 0.2 y el lightgreen por lightblue
        color = 'lightblue' if val <0.2 else 'white'
    if value==0.7:
        color = 'lightgreen' if np.abs(val)>=0.7 else 'white'
    if value==0.0:
        color = 'lightblue' if np.abs(val)<=0.05 else 'white'
#    elif value==0.8:
#        if val >=0.7 and val<0.8:
#            color = 'salmon'
#        elif val >=0.8:
#            color = 'lightblue' 
#        else:
#            color='white'

    return 'background-color: %s' % color

def stats_pair(data,metric,space,path,name_band,id,id_cross=None):
    databases=data['database'].unique().tolist()
    for DB in databases:
        data_DB=data[data['database']==DB]
        groups=data_DB['group'].unique()
        if len(groups)==1:
            databases.remove(DB)
    tablas={}
    for DB in databases:
        data_DB=data[data['database']==DB]
        combinaciones=[('Control', 'DTA'), ('G1', 'G2')]
        test_ez={}
        test_std={}
        for i in combinaciones:
            #Effect size
            ez=data_DB.groupby(['database',space]).apply(lambda data_DB:pg.compute_effsize(data_DB[data_DB['group']==i[0]][metric],data_DB[data_DB['group']==i[1]][metric])).to_frame()
            ez=ez.rename(columns={0:'effect size'})
            ez['A']=i[0]
            ez['B']=i[1]
            ez['Prueba']='effect size'
            test_ez['effsize-'+i[0]+'-'+i[1]]=ez
            #cv
            std=data_DB.groupby(['database',space]).apply(lambda data_DB:np.std(np.concatenate((data_DB[data_DB['group']==i[0]][metric],data_DB[data_DB['group']==i[1]][metric]),axis=0))).to_frame()
            std=std.rename(columns={0:'cv'})
            std['A']=i[0]
            std['B']=i[1]
            std['Prueba']='cv'
            test_std['cv-'+i[0]+'-'+i[1]]=std
            
        table_ez=pd.concat(list(test_ez.values()),axis=0)
        table_ez.reset_index( level = [0,1],inplace=True )
        table_std=pd.concat(list(test_std.values()),axis=0)
        table_std.reset_index( level = [0,1],inplace=True )
        table_concat=pd.concat([table_ez,table_std],axis=0)
        table=pd.pivot_table(table_concat,values=['effect size','cv'],columns=['Prueba'],index=['database',space,'A', 'B'])
        tablas[DB]=table
        table.columns=['effect size','cv']
        tablas[DB]=table
    table=pd.concat(list(tablas.values()),axis=0)
    if id_cross==None:
        path_complete='{path}\Graficos_{type}\{id}\{name_band}_{type}_{id}_table.png'.format(path=path,name_band=name_band,id=id,type=metric)  
    else:
        path_complete='{path}\Graficos_{type}\{id}\{name_band}_{id_cross}_{type}_{id}_table.png'.format(path=path,name_band=name_band,id=id,type=metric,id_cross=id_cross)
    save_table = table.copy()
    table=table.style.applymap(text_format,value=0.7,subset=['effect size']).applymap(text_format,value=0.0,subset=['cv'])
    #dfi.export(table, path_complete)
    return path_complete,save_table

def create_check(table,space,name_band,metric,state,mband=None):
    if state == 'different':
        #check = table[(np.abs(table['effect size']) > 0.7) & (np.abs(table['cv']) < 0.1)] 
        check = table[(np.abs(table['effect size']) > 0.7)] 
    else:
        #check = table[(np.abs(table['effect size']) <= 0.5) & (np.abs(table['cv']) < 0.1)]
        check = table[(np.abs(table['effect size']) <= 0.5)]
    check['space'] = space
    check['state'] = state
    check['band'] = name_band
    check['mband'] = mband
    check['metric'] = metric
    check = check.reset_index()
    return check

def std_poolsd(x,y):
    nx, ny = x.size, y.size
    dof = nx + ny - 2
    poolsd = np.sqrt(((nx - 1) * x.var(ddof=1) + (ny - 1) * y.var(ddof=1)) / dof)
    d = (x.mean() - y.mean()) / poolsd
    return d

def table_groups_DB(data,metric,space,path,name_band,id,id_cross=None):
    data=data[data['group']!='DCL'].copy()
    groups=data['group'].unique().tolist()
    tablas={}
    for g in groups:
        data_g=data[data['group']==g]
        databases=data_g['database'].unique()
        combinaciones = list(combinations(databases, 2))
        test_ez={}
        test_std={}
        for i in combinaciones:
            #Effect size
            ez=data_g.groupby(['group',space]).apply(lambda data_g:pg.compute_effsize(data_g[data_g['database']==i[0]][metric],data_g[data_g['database']==i[1]][metric])).to_frame()
            ez=ez.rename(columns={0:'effect size'})
            ez['A']=i[0]
            ez['B']=i[1]
            ez['Prueba']='effect size'
            test_ez['effsize-'+i[0]+'-'+i[1]]=ez
            #cv
            std=data_g.groupby(['group',space]).apply(lambda data_g:np.std(np.concatenate((data_g[data_g['database']==i[0]][metric],data_g[data_g['database']==i[1]][metric]),axis=0))).to_frame()
            std=std.rename(columns={0:'cv'})
            std['A']=i[0]
            std['B']=i[1]
            std['Prueba']='cv'
            test_std['cv-'+i[0]+'-'+i[1]]=std
        table_ez=pd.concat(list(test_ez.values()),axis=0)
        table_ez.reset_index( level = [0],inplace=True )
        table_std=pd.concat(list(test_std.values()),axis=0)
        table_std.reset_index( level = [0],inplace=True )
        table_concat=pd.concat([table_ez,table_std],axis=0)
        table=pd.pivot_table(table_concat,values=['effect size','cv'],columns=['Prueba'],index=['group',space,'A', 'B'])
        # table=table.T
        # table=table.swaplevel(0, 1)
        # table.sort_index(level=0,inplace=True)
        # table=table.T
        tablas[g]=table
        table.columns=['effect size','cv']
        tablas[g]=table
    table=pd.concat(list(tablas.values()),axis=0)
    if id_cross==None:
        path_complete='{path}\Graficos_{type}\{id}\{name_band}_{type}_{id}_table_DB.png'.format(path=path,name_band=name_band,id=id,type=metric)  
    else:
        path_complete='{path}\Graficos_{type}\{id}\{name_band}_{id_cross}_{type}_{id}_table_DB.png'.format(path=path,name_band=name_band,id=id,type=metric,id_cross=id_cross)
    save_table = table.copy()
    table=table.style.applymap(text_format,value=0.7,subset=['effect size']).applymap(text_format,value=0.0,subset=['cv'])
    #dfi.export(table, path_complete)
    return path_complete,save_table

def joinimages(paths):
    import sys
    from PIL import Image
    images =[Image.open(x) for x in paths]
    widths, heights = zip(*(i.size for i in images))
    total_width = sum(widths)
    max_height = max(heights)
    new_im = Image.new('RGB', (total_width, max_height))
    x_offset = 0
    for im in images:
        new_im.paste(im, (x_offset,0))
        x_offset += im.size[0]
    new_im.save(paths[1])
    print('Done!')