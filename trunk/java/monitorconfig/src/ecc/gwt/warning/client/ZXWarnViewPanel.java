package ecc.gwt.warning.client;

import java.util.ArrayList;
import java.util.Date;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.logging.Logger;



import com.extjs.gxt.ui.client.Style.HorizontalAlignment;
import com.extjs.gxt.ui.client.Style.SortDir;
import com.extjs.gxt.ui.client.core.XTemplate;
import com.extjs.gxt.ui.client.data.BaseListLoadConfig;
import com.extjs.gxt.ui.client.data.BaseListLoader;
import com.extjs.gxt.ui.client.data.BaseModelData;
import com.extjs.gxt.ui.client.data.BasePagingLoadConfig;
import com.extjs.gxt.ui.client.data.BasePagingLoadResult;
import com.extjs.gxt.ui.client.data.BasePagingLoader;
import com.extjs.gxt.ui.client.data.HttpProxy;
import com.extjs.gxt.ui.client.data.JsonLoadResultReader;
import com.extjs.gxt.ui.client.data.JsonPagingLoadResultReader;
import com.extjs.gxt.ui.client.data.ListLoadConfig;
import com.extjs.gxt.ui.client.data.ListLoadResult;
import com.extjs.gxt.ui.client.data.LoadEvent;
import com.extjs.gxt.ui.client.data.ModelData;
import com.extjs.gxt.ui.client.data.ModelType;
import com.extjs.gxt.ui.client.data.PagingLoadConfig;
import com.extjs.gxt.ui.client.data.PagingLoadResult;
import com.extjs.gxt.ui.client.data.PagingLoader;
import com.extjs.gxt.ui.client.event.ButtonEvent;
import com.extjs.gxt.ui.client.event.Events;
import com.extjs.gxt.ui.client.event.GridEvent;
import com.extjs.gxt.ui.client.event.Listener;
import com.extjs.gxt.ui.client.event.LoadListener;
import com.extjs.gxt.ui.client.event.RowEditorEvent;
import com.extjs.gxt.ui.client.event.SelectionListener;
import com.extjs.gxt.ui.client.store.ListStore;
import com.extjs.gxt.ui.client.widget.ContentPanel;
import com.extjs.gxt.ui.client.widget.DatePicker;
import com.extjs.gxt.ui.client.widget.LayoutContainer;
import com.extjs.gxt.ui.client.widget.MessageBox;
import com.extjs.gxt.ui.client.widget.Popup;
import com.extjs.gxt.ui.client.widget.button.Button;
import com.extjs.gxt.ui.client.widget.form.ComboBox;
import com.extjs.gxt.ui.client.widget.form.DateField;
import com.extjs.gxt.ui.client.widget.form.TextField;
import com.extjs.gxt.ui.client.widget.form.ComboBox.TriggerAction;
import com.extjs.gxt.ui.client.widget.grid.CellEditor;
import com.extjs.gxt.ui.client.widget.grid.ColumnConfig;
import com.extjs.gxt.ui.client.widget.grid.ColumnData;
import com.extjs.gxt.ui.client.widget.grid.ColumnModel;
import com.extjs.gxt.ui.client.widget.grid.Grid;
import com.extjs.gxt.ui.client.widget.grid.GridCellRenderer;
import com.extjs.gxt.ui.client.widget.grid.RowEditor;
import com.extjs.gxt.ui.client.widget.grid.RowNumberer;
import com.extjs.gxt.ui.client.widget.grid.EditorGrid.ClicksToEdit;
import com.extjs.gxt.ui.client.widget.layout.FitLayout;
import com.extjs.gxt.ui.client.widget.toolbar.LabelToolItem;
import com.extjs.gxt.ui.client.widget.toolbar.PagingToolBar;
import com.extjs.gxt.ui.client.widget.toolbar.SeparatorToolItem;
import com.extjs.gxt.ui.client.widget.toolbar.ToolBar;
import com.google.gwt.core.client.GWT;
import com.google.gwt.http.client.RequestBuilder;
import com.google.gwt.i18n.client.DateTimeFormat;
import com.google.gwt.i18n.client.NumberFormat;
import com.google.gwt.user.client.Element;
import com.google.gwt.user.client.rpc.AsyncCallback;

public class ZXWarnViewPanel extends LayoutContainer {

	private Logger logger;
	final private Grid<ModelData> grid;
	final private JsonRpc jsonRpc=new JsonRpc();
	final private ListStore<ModelData> alarmConfigList;
	final PagingToolBar toolBar = new PagingToolBar(25);  
	final DateTimeFormat sdf=DateTimeFormat.getFormat("yyyy-MM-dd");
	final private ListStore<ModelData> logLevelStore=UiUtil.generateStore(new String[]{"所有","1级告警","2级告警","3级告警","4级告警"},new String[]{"all","1","2","3","4"});
	public ZXWarnViewPanel() {
		logger=Logger.getLogger("ecc.gwt.warning.client");
		setLayout(new FitLayout());
		ModelType type = new ModelType();  
	    type.setRoot("records");
		type.addField("alarmName", "alarmName");
		type.addField("alarmTypeId", "alarmTypeId");
		type.addField("alarmLevel", "alarmLevel");
		String path =  GWT.getHostPageBaseURL()+ "zxWarn/getAlarmConfig.nut";
		RequestBuilder builder = new RequestBuilder(RequestBuilder.GET, path);  
	    HttpProxy<String> proxy = new HttpProxy<String>(builder); 
	    JsonLoadResultReader<ListLoadResult<ModelData>> reader=new JsonLoadResultReader<ListLoadResult<ModelData>>(type);
		final BaseListLoader<ListLoadResult<ModelData>> loader=new BaseListLoader<ListLoadResult<ModelData>>(proxy,reader); 
		 alarmConfigList=new ListStore<ModelData>(loader);
		 loader.load();
		grid=createGrid();
	}

	/* (non-Javadoc)
	 * @see com.extjs.gxt.ui.client.widget.LayoutContainer#onRender(com.google.gwt.user.client.Element, int)
	 */
	@Override
	protected void onRender(Element parent, int index) {
		super.onRender(parent, index);
	   
	    //grid.setSize(this.getWidth()-20, getHeight()-30);
	    ContentPanel panel=new ContentPanel();
	    panel.setHeaderVisible(false);
	    panel.setLayout(new FitLayout());
	    panel.setTopComponent(createToolBar());
	    panel.add(grid);
	    panel.setBottomComponent(toolBar);
	    panel.setAutoHeight(true);
	    panel.setAutoWidth(true);
	    add(panel);
	    
	}
	
	private ToolBar createToolBar(){
		
	    final DateField startDate=new DateField();
	    startDate.setValue(new Date());
	    final DateField endDate=new DateField();
	    endDate.setValue(new Date());
	    final ComboBox<ModelData> alarmLevel = new ComboBox<ModelData>();
	   
	    alarmLevel.setTriggerAction(TriggerAction.ALL);
	    alarmLevel.setEditable(false);
	    alarmLevel.setFireChangeEventOnSetValue(true);
	    alarmLevel.setWidth(100);
	    alarmLevel.setStore(logLevelStore);
	    alarmLevel.setDisplayField("name");
	    
	    final ComboBox<ModelData> alarmType = new ComboBox<ModelData>();
	    
	    
		
	    alarmType.setTriggerAction(TriggerAction.ALL);
	    alarmType.setEditable(false);
	    alarmType.setFireChangeEventOnSetValue(true);
	    alarmType.setWidth(100);
	    alarmType.setStore(alarmConfigList);
	    alarmType.setDisplayField("alarmName");
	    
	    Button searchButton=new Button("查询");
	    searchButton.addSelectionListener(new SelectionListener<ButtonEvent>(){

			@Override
			public void componentSelected(ButtonEvent ce) {
				String alarmLevelValue="";
				String alarmTypeStr="";
				if(alarmLevel.getValue()!=null)
					alarmLevelValue=alarmLevel.getValue().get("value");
				String startDateStr=sdf.format(startDate.getValue());
				String endDateStr=sdf.format(endDate.getValue());
				if(alarmType.getValue()!=null)
					alarmTypeStr=alarmType.getValue().get("alarmTypeId");
				//ListLoadConfig loadCofig=grid.getStore().getLoadConfig();
				PagingLoadConfig config = new BasePagingLoadConfig(); 
				config.setOffset(0);  
				config.setLimit(25);  
		            
		          Map<String, Object> state = grid.getState();  
		          /*if (state.containsKey("offset")) {  
		            int offset = (Integer)state.get("offset");  
		            int limit = (Integer)state.get("limit");  
		            config.setOffset(offset);  
		            config.setLimit(limit);  
		          }  */
		          if (state.containsKey("sortField")) {  
		        	  config.setSortField((String)state.get("sortField"));  
		        	  config.setSortDir(SortDir.valueOf((String)state.get("sortDir")));  
		          }  
		          config.set("alarmLevel", alarmLevelValue);
		          config.set("startDate", startDateStr);
		          config.set("endDate", endDateStr);
		          config.set("alarmTypeId", alarmTypeStr);
		          config.set("totalCount", "");
				  grid.getStore().getLoader().load(config);
				
			}
	    	
	    });
	    ToolBar toolBar = new ToolBar();
	    toolBar.add(new LabelToolItem("告警开始时间: "));
	    toolBar.add(startDate);
	    toolBar.add(new SeparatorToolItem());
	    toolBar.add(new LabelToolItem("告警结束时间: "));
	    toolBar.add(endDate);
	    
	   
	    
	    //toolBar.add(new FillToolItem());
	    toolBar.add(new LabelToolItem("告警级别: "));
	    toolBar.add(alarmLevel);
	    toolBar.add(new SeparatorToolItem());
	    toolBar.add(new LabelToolItem("告警类型: "));
	    toolBar.add(alarmType);
	    toolBar.add(new SeparatorToolItem());
	    toolBar.add(searchButton);
	    return toolBar;
	}
	
	private Grid createGrid(){
		List<ColumnConfig> columns = new ArrayList<ColumnConfig>();  
		ColumnConfig idColumnConfig=new ColumnConfig("seq", "ID",20);
		idColumnConfig.setHidden(true);
		//columns.add(new RowNumberer());
	    columns.add(idColumnConfig);  
	    ColumnConfig alarmSeqColumnConfig=new ColumnConfig("alarmSeq", "告警流水",130);
	    ColumnConfig alarmTypeIdColumnConfig=new ColumnConfig("alarmTypeId", "告警类型", 130);
	    ColumnConfig alarmLevelColumnConfig=new ColumnConfig("alarmLevel", "告警级别", 100);
	    ColumnConfig alarmTimeColumnConfig=new ColumnConfig("alarmTime", "告警时间", 150);
	    ColumnConfig logTypeConfig=new ColumnConfig("logType", "告警状态", 100);
	    logTypeConfig.setRenderer(new GridCellRenderer<ModelData>(){
			public Object render(ModelData model, String property,
					ColumnData config, int rowIndex, int colIndex,
					ListStore<ModelData> store, Grid<ModelData> grid) {
				String logType=model.get("logType");
				if("2".equals(logType))
					return "已恢复";
				else
					return "未恢复";
			}
	    	
	    });
	    ColumnConfig recoverTimeColumnConfig=new ColumnConfig("recoverTime", "恢复时间", 150);
	    ColumnConfig remarkColumnConfig=new ColumnConfig("remark", "备注", 150);
	    
	    alarmTypeIdColumnConfig.setRenderer(new GridCellRenderer<ModelData>(){
			public Object render(ModelData model, String property,
					ColumnData config, int rowIndex, int colIndex,
					ListStore<ModelData> store, Grid<ModelData> grid) {
				String alarmTypeId=model.get("alarmTypeId");
				ModelData alarmTypeIdMD=alarmConfigList.findModel("alarmTypeId", alarmTypeId);
				if(alarmTypeIdMD!=null)
					return alarmTypeIdMD.get("alarmName");
				else
					return alarmTypeId;
			}
	    	
	    });
	    
	    alarmLevelColumnConfig.setRenderer(new GridCellRenderer<ModelData>(){
			public Object render(ModelData model, String property,
					ColumnData config, int rowIndex, int colIndex,
					ListStore<ModelData> store, Grid<ModelData> grid) {
				String alarmLevel=model.get("alarmLevel");
				ModelData alarmLevelMD=logLevelStore.findModel("value", alarmLevel);
				if(alarmLevelMD!=null)
					return alarmLevelMD.get("name");
				else
					return alarmLevel;
			}
	    	
	    });
	    columns.add(new RowNumberer());
	    columns.add(alarmSeqColumnConfig);
	    columns.add(alarmTypeIdColumnConfig);  
	    columns.add(alarmLevelColumnConfig);  
	    columns.add(alarmTimeColumnConfig);
	    columns.add(logTypeConfig);
	    columns.add(recoverTimeColumnConfig);
	    columns.add(remarkColumnConfig);
	    
	    
	    ColumnModel cm = new ColumnModel(columns);
	    ModelType type = new ModelType();  
	    type.setRoot("records");
		type.addField("alarmSeq", "alarmSeq");
		type.addField("alarmTypeId", "alarmTypeId");
		type.addField("alarmLevel", "alarmLevel");
		type.addField("alarmTime", "alarmTime");
		type.addField("logType", "logType");
		type.addField("recoverTime", "recoverTime");
		type.addField("remark", "remark");
		type.setTotalName("total");
	    String path =  GWT.getHostPageBaseURL()+ "zxWarn/getAlarmLog.nut";
	    RequestBuilder builder = new RequestBuilder(RequestBuilder.GET, path);  
	    HttpProxy<String> proxy = new HttpProxy<String>(builder); 
	    JsonPagingLoadResultReader<BasePagingLoadResult<ModelData>> reader=new JsonPagingLoadResultReader <BasePagingLoadResult<ModelData>>(type);
		final BasePagingLoader<BasePagingLoadResult<ModelData>> loader=new BasePagingLoader<BasePagingLoadResult<ModelData>>(proxy,reader); 
		final ListStore<ModelData> store=new ListStore<ModelData>(loader);
		final Grid<ModelData> grid = new Grid<ModelData>(store, cm);  
		grid.setStateId("pagingGridExample");  
		grid.setStateful(true);
		loader.addLoadListener(new LoadListener(){

			/* (non-Javadoc)
			 * @see com.extjs.gxt.ui.client.event.LoadListener#loaderBeforeLoad(com.extjs.gxt.ui.client.data.LoadEvent)
			 */
			@Override
			public void loaderBeforeLoad(LoadEvent le) {
				super.loaderBeforeLoad(le);
				if (loader.getLastConfig() instanceof PagingLoadConfig) {
					PagingLoadConfig config = (PagingLoadConfig) loader.getLastConfig();
					if(!config.getProperties().containsKey("totalCount"))
						config.set("totalCount", loader.getTotalCount());
				}
				
			}
			
		});
	    toolBar.bind(loader);
	    /*grid.addListener(Events.Attach, new Listener<GridEvent<ModelData>>() {  
	        public void handleEvent(GridEvent<ModelData> be) {  
	          //PagingLoadConfig config = new BasePagingLoadConfig();  
	          loader.setOffset(0);  
	          loader.setLimit(50);  
	            
	          Map<String, Object> state = grid.getState();  
	          if (state.containsKey("offset")) {  
	            int offset = (Integer)state.get("offset");  
	            int limit = (Integer)state.get("limit");  
	            loader.setOffset(offset);  
	            loader.setLimit(limit);  
	          }  
	          if (state.containsKey("sortField")) {  
	        	  loader.setSortField((String)state.get("sortField"));  
	        	  loader.setSortDir(SortDir.valueOf((String)state.get("sortDir")));  
	          }  
	          loader.load();  
	        }  
	      });  */
	    grid.setBorders(true);  
	    grid.setLoadMask(true);  
	    
	   // loader.load();
	    //grid.setSize(800, 350);
	    grid.setAutoWidth(true);
	    grid.setAutoExpandColumn("remark");
	    grid.setHeight(500);
	return grid;
	}
	
	
	

}
