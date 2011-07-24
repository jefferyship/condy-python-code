package ecc.gwt.warning.client;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.logging.Logger;

import org.mortbay.log.Log;


import com.extjs.gxt.ui.client.Style.HorizontalAlignment;
import com.extjs.gxt.ui.client.core.XTemplate;
import com.extjs.gxt.ui.client.data.BaseListLoadConfig;
import com.extjs.gxt.ui.client.data.BaseListLoader;
import com.extjs.gxt.ui.client.data.BaseModelData;
import com.extjs.gxt.ui.client.data.HttpProxy;
import com.extjs.gxt.ui.client.data.JsonLoadResultReader;
import com.extjs.gxt.ui.client.data.ListLoadConfig;
import com.extjs.gxt.ui.client.data.ListLoadResult;
import com.extjs.gxt.ui.client.data.ModelData;
import com.extjs.gxt.ui.client.data.ModelType;
import com.extjs.gxt.ui.client.event.ButtonEvent;
import com.extjs.gxt.ui.client.event.EventType;
import com.extjs.gxt.ui.client.event.Events;
import com.extjs.gxt.ui.client.event.Listener;
import com.extjs.gxt.ui.client.event.MessageBoxEvent;
import com.extjs.gxt.ui.client.event.RowEditorEvent;
import com.extjs.gxt.ui.client.event.SelectionChangedEvent;
import com.extjs.gxt.ui.client.event.SelectionChangedListener;
import com.extjs.gxt.ui.client.event.SelectionListener;
import com.extjs.gxt.ui.client.store.ListStore;
import com.extjs.gxt.ui.client.util.Format;
import com.extjs.gxt.ui.client.util.Params;
import com.extjs.gxt.ui.client.widget.ContentPanel;
import com.extjs.gxt.ui.client.widget.LayoutContainer;
import com.extjs.gxt.ui.client.widget.MessageBox;
import com.extjs.gxt.ui.client.widget.Popup;
import com.extjs.gxt.ui.client.widget.Window;
import com.extjs.gxt.ui.client.widget.button.Button;
import com.extjs.gxt.ui.client.widget.form.ComboBox;
import com.extjs.gxt.ui.client.widget.form.FormPanel;
import com.extjs.gxt.ui.client.widget.form.HiddenField;
import com.extjs.gxt.ui.client.widget.form.Radio;
import com.extjs.gxt.ui.client.widget.form.RadioGroup;
import com.extjs.gxt.ui.client.widget.form.SimpleComboBox;
import com.extjs.gxt.ui.client.widget.form.TextArea;
import com.extjs.gxt.ui.client.widget.form.TextField;
import com.extjs.gxt.ui.client.widget.form.ComboBox.TriggerAction;
import com.extjs.gxt.ui.client.widget.form.FormPanel.Method;
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
import com.extjs.gxt.ui.client.widget.toolbar.FillToolItem;
import com.extjs.gxt.ui.client.widget.toolbar.LabelToolItem;
import com.extjs.gxt.ui.client.widget.toolbar.SeparatorToolItem;
import com.extjs.gxt.ui.client.widget.toolbar.ToolBar;
import com.google.gwt.core.client.GWT;
import com.google.gwt.http.client.RequestBuilder;
import com.google.gwt.i18n.client.NumberFormat;
import com.google.gwt.user.client.Element;
import com.google.gwt.user.client.rpc.AsyncCallback;

public class WebServerConfigGrid extends LayoutContainer {

	private Logger logger;
	final private Grid<ModelData> grid;
	final private JsonRpc jsonRpc=new JsonRpc();
	public WebServerConfigGrid() {
		logger=Logger.getLogger("ecc.gwt.warning.client");
		setLayout(new FitLayout());
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
	    panel.setAutoHeight(true);
	    panel.setAutoWidth(true);
	    add(panel);
	    
	}
	
	private ToolBar createToolBar(){
		Button createRecordButton=new Button("增加");
		Button deleteRecordButton=new Button("删除");
		Button copyRecordButton=new Button("复制");
		final Window window=createAdd();
	    createRecordButton.addSelectionListener(new SelectionListener<ButtonEvent>(){
			@Override
			public void componentSelected(ButtonEvent ce) {
				window.show();
			}
	    });
	    deleteRecordButton.addSelectionListener(new SelectionListener<ButtonEvent>(){
			@Override
			public void componentSelected(ButtonEvent ce) {
					final ModelData modelData;
					if(grid.getSelectionModel().getSelectedItem()==null){
						MessageBox.alert("警告", "请选择需要删除的行", null);
						return; 
					}
					modelData=grid.getSelectionModel().getSelectedItem();
					MessageBox.confirm("提示", "确认要删除<"+modelData.get("monitorName")+">吗?", new Listener<MessageBoxEvent>(){

						public void handleEvent(MessageBoxEvent be) {
							if (!"Yes".equals(be.getButtonClicked().getText())){
								return ;
							}
							else{
								AsyncCallback deleteRecordCallBack=new AsyncCallback(){
									public void onFailure(Throwable caught) {
										MessageBox.alert("alert",caught.getMessage(),null);
									}
									public void onSuccess(Object result) {
										if((Boolean)result){
											grid.getStore().remove(modelData);
											MessageBox.info("提示", "删除成功", null);
										}else{
											MessageBox.info("提示","删除失败",null);
										}
										
									}
								};
								jsonRpc.request(GWT.getHostPageBaseURL()+ "monitorAsserver/delete.nut", modelData.getProperties(), deleteRecordCallBack);
							}
						}
						
					});
					
				
				
			}
	    });
	    copyRecordButton.addSelectionListener(new SelectionListener<ButtonEvent>(){
			@Override
			public void componentSelected(ButtonEvent ce) {
				final ModelData modelData=new BaseModelData();
				if(grid.getSelectionModel().getSelectedItem()==null){
					MessageBox.alert("警告", "请选择需要删除的行", null);
					return; 
				}
				ModelData willBeCopyModelData=grid.getSelectionModel().getSelectedItem();
				//获取新的一个ModelData。
				for (Iterator iterator = willBeCopyModelData.getPropertyNames().iterator(); iterator
						.hasNext();) {
					String name = (String) iterator.next();
					modelData.set(name, willBeCopyModelData.get(name));
				}
				MessageBox.confirm("提示", "确认要复制<"+modelData.get("monitorName")+">吗?", new Listener<MessageBoxEvent>(){
					public void handleEvent(MessageBoxEvent be) {
						if (!"Yes".equals(be.getButtonClicked().getText())){
							return ;
						}
						else{
							modelData.remove("seq");
							modelData.set("monitorName", (String)modelData.get("monitorName")+"_拷贝");
							AsyncCallback copyRecordCallBack=new AsyncCallback(){
								public void onFailure(Throwable caught) {
									MessageBox.alert("alert",caught.getMessage(),null);
								}
								public void onSuccess(Object result) {
									modelData.set("seq", result);
									grid.getStore().insert(modelData, 0);
									MessageBox.info("提示", "复制成功", null);
									
								}
							};
							jsonRpc.requestStream(GWT.getHostPageBaseURL()+ "monitorAsserver/insert.nut", modelData.getProperties(), copyRecordCallBack);
						}
					}
					
				});
			}
	    	
	    });
	    final ComboBox<ModelData> searchType = new ComboBox<ModelData>();
	    ListStore<ModelData> searchTypeStore=UiUtil.generateStore(new String[]{"扫描名称","地址"},new String[]{"monitorName","url"});
	    searchType.setTriggerAction(TriggerAction.ALL);
	    searchType.setEditable(false);
	    searchType.setFireChangeEventOnSetValue(true);
	    searchType.setWidth(100);
	    searchType.setStore(searchTypeStore);
	    searchType.setDisplayField("name");
	    /*searchType.add("扫描名称");
	    searchType.add("地址");
	    searchType.setSimpleValue("地址");*/
	    final TextField<String> searchContent=new TextField<String>();
	    searchContent.setWidth(300);
	    Button searchButton=new Button("查询");
	    searchButton.addSelectionListener(new SelectionListener<ButtonEvent>(){

			@Override
			public void componentSelected(ButtonEvent ce) {
				String sSearchType=searchType.getValue().get("value");
				logger.info("searchType"+sSearchType);
				logger.info("searchContent"+searchContent.getValue());
				
					ListLoadConfig loadCofig=grid.getStore().getLoadConfig();
					loadCofig.set("searchType", sSearchType);
					loadCofig.set("searchContent", searchContent.getValue());
					grid.getStore().getLoader().load(loadCofig);
				
			}
	    	
	    });
	    ToolBar toolBar = new ToolBar();
	    toolBar.add(createRecordButton);
	    toolBar.add(new SeparatorToolItem());
	    toolBar.add(deleteRecordButton);
	    toolBar.add(new SeparatorToolItem());
	    toolBar.add(copyRecordButton);
	    
	    toolBar.add(new FillToolItem());
	    toolBar.add(new LabelToolItem("查询类型: "));
	    toolBar.add(searchType);
	    toolBar.add(searchContent);
	    
	    toolBar.add(searchButton);
	    return toolBar;
	}
	
	private Grid createGrid(){
		List<ColumnConfig> columns = new ArrayList<ColumnConfig>();  
		ColumnConfig idColumnConfig=new ColumnConfig("seq", "ID",20);
		idColumnConfig.setHidden(true);
		//columns.add(new RowNumberer());
	    columns.add(idColumnConfig);  
	    ColumnConfig monitorNameColumnConfig=new ColumnConfig("monitorName", "扫描名称",130);
	    ColumnConfig urlContentColumnConfig=new ColumnConfig("urlContent", "测试参数", 380);
	    ColumnConfig aboutSystemColumnConfig=new ColumnConfig("aboutSystem", "关联系统", 100);
	    ColumnConfig urlColumnConfig=new ColumnConfig("url", "地址", 320);
	    ColumnConfig stsColumnConfig=new ColumnConfig("sts", "状态", 60);
	    aboutSystemColumnConfig.setEditor(new CellEditor(new TextField<String>()));
	    monitorNameColumnConfig.setEditor(new CellEditor(new TextField<String>()));
	    urlContentColumnConfig.setEditor(new CellEditor(new TextField<String>()));
	    urlColumnConfig.setEditor(new CellEditor(new TextField<String>()));
	    ListStore<ModelData> stsStore=UiUtil.generateStore(new String[]{"在用","不在用"},new String[]{"A","B"});
	    final ComboBox<ModelData> stsType = new ComboBox<ModelData>();
	    stsType.setStore(stsStore);
	    stsType.setTriggerAction(TriggerAction.ALL);
	    stsType.setEditable(false);
	    stsType.setFireChangeEventOnSetValue(true);
	    stsType.setWidth(60);
	    stsType.setDisplayField("name");
	    stsType.setValueField("value");
	   // stsType.add("A");
	    //stsType.add("B");
	    CellEditor stsEditor = new CellEditor(stsType) {  
	        @Override  
	        public Object preProcessValue(Object value) {  
	          if (value == null) {  
	            return value;  
	          }  
	          return stsType.getStore().findModel("value", value);
	        }  
	    
	        @Override  
	        public Object postProcessValue(Object value) {  
	          if (value == null) {  
	            return value;  
	          }  
	          return ((ModelData) value).get("value");  
	        }  
	      };  
	    stsColumnConfig.setEditor(stsEditor);
	    columns.add(new RowNumberer());
	    columns.add(monitorNameColumnConfig);
	    columns.add(urlColumnConfig);  
	    columns.add(urlContentColumnConfig);  
	    columns.add(aboutSystemColumnConfig);
	    
	    stsColumnConfig.setRenderer(new GridCellRenderer<ModelData>(){
			public Object render(ModelData model, String property,
					ColumnData config, int rowIndex, int colIndex,
					ListStore<ModelData> store, Grid<ModelData> grid) {
				String sts=model.get("sts");
				if("A".equals(sts))
					return "在用";
				else
					return "不在用";
			}
	    	
	    });
	    columns.add(stsColumnConfig);
	    ColumnModel cm = new ColumnModel(columns);
	    ModelType type = new ModelType();  
	    type.setRoot("records");
		type.addField("monitorName", "monitorName");
		type.addField("seq", "seq");
		type.addField("url", "url");
		type.addField("urlContent", "urlContent");
		type.addField("sts", "sts");
		type.addField("aboutSystem", "aboutSystem");
	    String path =  GWT.getHostPageBaseURL()+ "monitorAsserver/list.nut";
	    RequestBuilder builder = new RequestBuilder(RequestBuilder.GET, path);  
	    HttpProxy<String> proxy = new HttpProxy<String>(builder); 
	    JsonLoadResultReader<ListLoadResult<ModelData>> reader=new JsonLoadResultReader<ListLoadResult<ModelData>>(type);
		final BaseListLoader<ListLoadResult<ModelData>> loader=new BaseListLoader<ListLoadResult<ModelData>>(proxy,reader); 
		final ListStore<ModelData> store=new ListStore<ModelData>(loader);
		final RowEditor<ModelData> rowEditor=new RowEditor<ModelData>();
		Grid<ModelData> grid = new Grid<ModelData>(store, cm);  
	    rowEditor.setClicksToEdit(ClicksToEdit.TWO);
	    rowEditor.getMessages().setSaveText("提交");
	    rowEditor.getMessages().setCancelText("取消");
	    rowEditor.addListener(Events.AfterEdit,new Listener<RowEditorEvent>(){
			public void handleEvent(RowEditorEvent be) {
				ModelData modelData=store.getAt(be.getRowIndex());
				AsyncCallback modifyRecordCallBack=new AsyncCallback(){
					public void onFailure(Throwable caught) {
						store.rejectChanges();
						MessageBox.alert("alert",caught.getMessage(),null);
					}
					public void onSuccess(Object result) {
						if((Boolean)result){
							store.commitChanges();
							MessageBox.alert("alert","修改成功",null);
						}else{
							store.rejectChanges();
							MessageBox.alert("alert","修改失败",null);
						}
						
					}
				};
			jsonRpc.requestStream(GWT.getHostPageBaseURL()+ "monitorAsserver/update.nut", modelData.getProperties(), modifyRecordCallBack);
			}
	    	
	    });
	    grid.setBorders(true);  
	    grid.setLoadMask(true);  
	    grid.addPlugin(rowEditor);
	    grid.setAutoExpandColumn("urlContent");
	    loader.load();
	    //grid.setSize(800, 350);
	    grid.setAutoWidth(true);
	    grid.setHeight(500);
	return grid;
	}
	
	private Window createAdd(){
		final Window window=new Window();
		window.setHeading("增加记录");
		window.setSize(350, 300);
		window.setResizable(true);
		window.setLayout(new FitLayout());
		final FormPanel formPanel=new FormPanel();
		formPanel.setHeaderVisible(false);
		final HiddenField<String> seqField=new HiddenField<String>();
		seqField.setValue("0");
		final TextArea urlField=new TextArea();
		urlField.setFieldLabel("地址");
		urlField.setAllowBlank(false);
		urlField.setValue("iserv/CallUrcp.jsp");
		urlField.setToolTip("类似:http://ip:port/上下文根/iserv/CalllUrcp.jsp");
		final TextField<String> monitorNameField=new TextField<String>();
		monitorNameField.setFieldLabel("扫描名称");
		monitorNameField.setAllowBlank(false);
		final TextArea urlContentField=new TextArea();
		urlContentField.setFieldLabel("测试参数");
		urlContentField.setAllowBlank(false);
		urlContentField.setValue("name=getRouteInfo&param=88203511100000591101001");
		urlContentField.setToolTip("类似:name=服务名&param=以chr(1)做分隔符的输入参数");
		final TextField<String> aboutSystemField=new TextField<String>();
		String[] names=new String[]{"CJ","转人工路由","CRM","门户接口机"};
		String[] values=new String[]{"name=TCCS_F_POS_BLACK&param=8820351109020591",//CJ
								"name=getRouteInfo&param=88203511100000591101001",//转人工路由
								"name=GetServiceInfoUnion&param=836571780591",//CRM
								"name=getRouteInfo&param=88203511100000591101001"};//门户接口机
		ListStore<ModelData> aboutSystemStore=UiUtil.generateStore(names,values);
		final ComboBox<ModelData> aboutSystemCombo = new ComboBox<ModelData>();
		aboutSystemCombo.setFieldLabel("测试参数类型");
		aboutSystemCombo.setDisplayField("name");
		aboutSystemCombo.setStore(aboutSystemStore);
		aboutSystemCombo.setTriggerAction(TriggerAction.ALL);
		aboutSystemCombo.setEditable(false);
		aboutSystemCombo.setFireChangeEventOnSetValue(true);
		aboutSystemCombo.setDisplayField("name");
		aboutSystemCombo.setValueField("value");
		aboutSystemCombo.addSelectionChangedListener(new SelectionChangedListener<ModelData>() {
			@Override
			public void selectionChanged(SelectionChangedEvent<ModelData> se) {
				urlContentField.setValue((String)se.getSelectedItem().get("value"));
			}
			
		});
		aboutSystemField.setFieldLabel("关联系统");
		aboutSystemField.setAllowBlank(false);
		final TextField<String> areaCodeField=new TextField<String>();
		areaCodeField.setFieldLabel("地区");
		areaCodeField.setValue("0591");
		final Radio noUsedRadio=new Radio();
		noUsedRadio.setBoxLabel("不在用");
		final Radio usedRadio=new Radio();
		usedRadio.setBoxLabel("在用");
		final RadioGroup stsRadioGroup=new RadioGroup();
		stsRadioGroup.add(usedRadio);
		stsRadioGroup.add(noUsedRadio);
		stsRadioGroup.setValue(noUsedRadio);
		stsRadioGroup.setFieldLabel("状态");
		formPanel.add(monitorNameField);
		formPanel.add(urlField);
		formPanel.add(aboutSystemCombo);
		formPanel.add(urlContentField);
		formPanel.add(aboutSystemField);
		formPanel.add(areaCodeField);
		formPanel.add(stsRadioGroup);
		formPanel.setAction("");
		Button submitButton=new Button("提交");
		submitButton.addSelectionListener(new SelectionListener<ButtonEvent>(){

			@Override
			public void componentSelected(ButtonEvent ce) {
				if (formPanel.isValid()){
					final Map<String,Object> modelDataMap=new HashMap<String,Object>();
					modelDataMap.put("monitorName", monitorNameField.getValue());
					modelDataMap.put("url", urlField.getValue());
					modelDataMap.put("urlContent", urlContentField.getValue());
					modelDataMap.put("aboutSystem", aboutSystemField.getValue());
					modelDataMap.put("areaCode", areaCodeField.getValue());
					if(stsRadioGroup.getValue().equals(usedRadio))
						modelDataMap.put("sts", "A");
					else
						modelDataMap.put("sts", "B");
					AsyncCallback addRecordCallBack=new AsyncCallback(){
						public void onFailure(Throwable caught) {
							MessageBox.alert("alert",caught.getMessage(),null);
						}
						public void onSuccess(Object result) {
							modelDataMap.put("seq", String.valueOf(result));
							final ModelData modelData=new BaseModelData(modelDataMap);
							//modelData.set("seq", (Integer)result); 
							grid.getStore().insert(modelData,0);
							MessageBox.alert("alert","操作成功",null);
							window.hide();
							
						}
					};
					jsonRpc.requestStream(GWT.getHostPageBaseURL()+ "monitorAsserver/insert.nut", modelDataMap, addRecordCallBack);
					
					
				}
				
				
			}
			
		});
			
		formPanel.addButton(submitButton);
		formPanel.setButtonAlign(HorizontalAlignment.CENTER);
		window.add(formPanel);
		
		return window;
	}
	

}
