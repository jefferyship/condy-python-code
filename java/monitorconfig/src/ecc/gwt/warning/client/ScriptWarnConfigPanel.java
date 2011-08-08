package ecc.gwt.warning.client;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.logging.Logger;


import com.extjs.gxt.ui.client.Registry;
import com.extjs.gxt.ui.client.Style.LayoutRegion;
import com.extjs.gxt.ui.client.Style.Scroll;
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
import com.extjs.gxt.ui.client.event.Events;
import com.extjs.gxt.ui.client.event.GridEvent;
import com.extjs.gxt.ui.client.event.Listener;
import com.extjs.gxt.ui.client.event.MessageBoxEvent;
import com.extjs.gxt.ui.client.event.SelectionListener;
import com.extjs.gxt.ui.client.store.ListStore;
import com.extjs.gxt.ui.client.widget.ContentPanel;
import com.extjs.gxt.ui.client.widget.LayoutContainer;
import com.extjs.gxt.ui.client.widget.MessageBox;
import com.extjs.gxt.ui.client.widget.Window;
import com.extjs.gxt.ui.client.widget.button.Button;
import com.extjs.gxt.ui.client.widget.form.ComboBox;
import com.extjs.gxt.ui.client.widget.form.FormPanel;
import com.extjs.gxt.ui.client.widget.form.HiddenField;
import com.extjs.gxt.ui.client.widget.form.TextArea;
import com.extjs.gxt.ui.client.widget.form.TextField;
import com.extjs.gxt.ui.client.widget.form.ComboBox.TriggerAction;
import com.extjs.gxt.ui.client.widget.form.FormPanel.LabelAlign;
import com.extjs.gxt.ui.client.widget.grid.ColumnConfig;
import com.extjs.gxt.ui.client.widget.grid.ColumnData;
import com.extjs.gxt.ui.client.widget.grid.ColumnModel;
import com.extjs.gxt.ui.client.widget.grid.Grid;
import com.extjs.gxt.ui.client.widget.grid.GridCellRenderer;
import com.extjs.gxt.ui.client.widget.layout.BorderLayout;
import com.extjs.gxt.ui.client.widget.layout.BorderLayoutData;
import com.extjs.gxt.ui.client.widget.layout.ColumnLayout;
import com.extjs.gxt.ui.client.widget.layout.FormData;
import com.extjs.gxt.ui.client.widget.layout.FormLayout;
import com.extjs.gxt.ui.client.widget.toolbar.SeparatorToolItem;
import com.extjs.gxt.ui.client.widget.toolbar.ToolBar;
import com.google.gwt.core.client.GWT;
import com.google.gwt.http.client.RequestBuilder;
import com.google.gwt.user.client.Element;
import com.google.gwt.user.client.rpc.AsyncCallback;
/**
 * 
 * @author 林桦
 *
 */
public class ScriptWarnConfigPanel extends LayoutContainer {
	private Logger logger;
	final private JsonRpc jsonRpc=new JsonRpc();
	final private Grid<ModelData> planGrid;
	final Window scriptWarningPersonPopup;
	final ScriptWarningScriptPopup scriptWarningScriptPopup;
	//FormPanel的对象.
	final FormPanel planPanel=new FormPanel();
	final TextField<String> planNameField=new TextField<String>();
	final TextField<String> remarkField=new TextField<String>();
	final ComboBox<ModelData> beginHoursCombo = new ComboBox<ModelData>();
    final TextField<String> lasttTimeField=new TextField<String>();
    final ComboBox<ModelData> runStsCombo = new ComboBox<ModelData>();
    final ComboBox<ModelData> endHoursCombo = new ComboBox<ModelData>();
    final TextField<String> nextTimeField=new TextField<String>();
    final ComboBox<ModelData> stsCombo = new ComboBox<ModelData>();
    final TextField<String> planIdField=new TextField<String>();
    final TextField<String> companyIdField=new TextField<String>();
    final TextField<String> areaCodeField=new TextField<String>();
    final TextField<String> dataTagField=new TextField<String>();
    final TextField<Integer> runCycleField=new TextField<Integer>();
    final HiddenField<String> actionTypeField=new HiddenField<String>();
    //脚本的Area
    final TextArea scriptArea=new TextArea();
    
	
	public ScriptWarnConfigPanel(){
		logger=Logger.getLogger("ecc.gwt.warning.client.ScriptWarnConfigPanel");
		BorderLayout borderLayout=new BorderLayout();
		setLayout(borderLayout);
		planGrid=generatePlanGrid();
		scriptWarningPersonPopup=new ScriptWarningPersonPopup(planGrid);
		scriptWarningScriptPopup=new ScriptWarningScriptPopup(planGrid);
		
		
	}
	
	protected void onRender(Element parent, int index) {
		super.onRender(parent, index);
		ContentPanel westPanel=new ContentPanel();
		westPanel.setAutoHeight(true);
		westPanel.setAutoWidth(true);
		westPanel.add(planGrid);
		westPanel.setHeading("计划列表");
		BorderLayoutData westLayoutData=new BorderLayoutData(LayoutRegion.WEST,205,150,300);
		westLayoutData.setSplit(true);
		westLayoutData.setCollapsible(true);
		//westLayoutData.setMargins(new Margins(5));
		BorderLayoutData centerLayoutData=new BorderLayoutData(LayoutRegion.CENTER);
		add(westPanel,westLayoutData);
	    //centerLayoutData.setMargins(new Margins(5));
	    add(centerPanel(),centerLayoutData);
	    
	}
	
	private void isFormFieldReadOnly(boolean realOnly){
		planNameField.setReadOnly(realOnly);
		remarkField.setReadOnly(realOnly);
		beginHoursCombo.setReadOnly(realOnly);
		lasttTimeField.setReadOnly(realOnly);
		runStsCombo.setReadOnly(realOnly);
		endHoursCombo.setReadOnly(realOnly);
		nextTimeField.setReadOnly(realOnly);
		stsCombo.setReadOnly(realOnly);
		companyIdField.setReadOnly(realOnly);
		areaCodeField.setReadOnly(realOnly);
		dataTagField.setReadOnly(realOnly);
		runCycleField.setReadOnly(realOnly);
		
	}
	private Grid<ModelData> generatePlanGrid(){
		ColumnConfig planNameColumnConfig=new ColumnConfig("planName", "计划名称",130);
	    ColumnConfig runStsColumnConfig=new ColumnConfig("runStatus", "运行状态", 70);
	    runStsColumnConfig.setRenderer(new GridCellRenderer<ModelData>(){
			public Object render(ModelData model, String property,
					ColumnData config, int rowIndex, int colIndex,
					ListStore<ModelData> store, Grid<ModelData> grid) {
				String sts=model.get("runStatus");
				if("A".equals(sts))
					return "在用";
				else
					return "不在用";
			}
	    	
	    });
	    List<ColumnConfig> columns = new ArrayList<ColumnConfig>();  
	    columns.add(planNameColumnConfig);
	    columns.add(runStsColumnConfig);  
	    ColumnModel cm = new ColumnModel(columns);
	    
		ModelType type = new ModelType();  
	    type.setRoot("records");
		type.addField("planName", "planName");
		type.addField("areaCode", "areaCode");
		type.addField("planId", "planId");
		type.addField("companyId", "companyId");
		type.addField("remark", "remark");
		type.addField("runCycle", "runCycle");
		type.addField("runStatus", "runStatus");
		type.addField("lastTime", "lastTime");
		type.addField("nextTime", "nextTime");
		type.addField("beginHours", "beginHours");
		type.addField("endHours", "endHours");
		type.addField("scriptId", "scriptId");
		type.addField("dataTagId", "dataTagId");
		type.addField("sts", "sts");
		String path =  GWT.getHostPageBaseURL()+ "scriptWarnAction/warnPlanList.nut";
	    RequestBuilder builder = new RequestBuilder(RequestBuilder.GET, path);  
	    HttpProxy<String> proxy = new HttpProxy<String>(builder); 
	    JsonLoadResultReader<ListLoadResult<ModelData>> reader=new JsonLoadResultReader<ListLoadResult<ModelData>>(type);
		final BaseListLoader<ListLoadResult<ModelData>> loader=new BaseListLoader<ListLoadResult<ModelData>>(proxy,reader); 
		final ListStore<ModelData> listStore=new ListStore<ModelData>(loader);
		
		Grid<ModelData> grid = new Grid<ModelData>(listStore, cm);  
		//GridSelectionModel<ModelData> sm=new GridSelectionModel<ModelData>();
		//sm.setSelectionMode(SelectionMode.SIMPLE);
		//grid.setSelectionModel(sm);
		grid.setHeight(515);
		grid.setAutoWidth(true);
		grid.addListener(Events.RowClick, new Listener<GridEvent<ModelData>>(){

			public void handleEvent(GridEvent<ModelData> be) {
				ModelData md=be.getModel();
				//赋值
				isFormFieldReadOnly(true);
				planNameField.setValue((String)md.get("planName"));
				remarkField.setValue((String)md.get("remark"));
				ModelData startHourModelData=beginHoursCombo.getStore().findModel("value", (String)md.get("beginHours"));
				beginHoursCombo.setValue(startHourModelData);
				lasttTimeField.setValue((String)md.get("lastTime"));
				ModelData runStsModelData=runStsCombo.getStore().findModel("value", (String)md.get("runStatus"));
				runStsCombo.setValue(runStsModelData);
				ModelData endHourModelData=endHoursCombo.getStore().findModel("value", (String)md.get("endHours"));
				endHoursCombo.setValue(endHourModelData);
				nextTimeField.setValue((String)md.get("nextTime"));
				ModelData stsModelData=stsCombo.getStore().findModel("value", (String)md.get("sts"));
				stsCombo.setValue(stsModelData);
				planIdField.setValue((String)md.get("planId"));
				companyIdField.setValue((String)md.get("companyId"));
				areaCodeField.setValue((String)md.get("areaCode"));
				dataTagField.setValue((String)md.get("dataTagId"));
				runCycleField.setValue(Integer.parseInt((String)md.get("runCycle")));
				
				ListStore<ModelData> listStore=(ListStore<ModelData>)Registry.get("PERSON_WARN_STORE");
				ListLoadConfig llc=new BaseListLoadConfig();
				llc.set("planId", (String)md.get("planId"));
				listStore.getLoader().load(llc);
				AsyncCallback getScriptCallBack=new AsyncCallback(){
					public void onFailure(Throwable caught) {
						MessageBox.alert("alert",caught.getMessage(),null);
					}
					public void onSuccess(Object result) {
						Map warnScriptMap=(Map)result;
						scriptArea.setValue((String)warnScriptMap.get("scriptbash"));
						
					}
				};
				Map<String,String> inputParamMap=new HashMap<String,String>();
				if(!"".equals(md.get("scriptId"))&&md.get("scriptId")!=null){
					inputParamMap.put("scriptId", (String)md.get("scriptId"));
					jsonRpc.request(GWT.getHostPageBaseURL()+ "scriptWarnAction/getWarnScript.nut", inputParamMap, getScriptCallBack);
				}
				
			}
			
		});
		loader.load();
		return grid;
		
	}
	
	private ContentPanel centerPanel(){
		ContentPanel centerPanel=new ContentPanel();
		centerPanel.setHeaderVisible(false);
		centerPanel.setScrollMode(Scroll.AUTO);
		centerPanel.add(planPanel());
		LayoutContainer mainContainer=new LayoutContainer();
		mainContainer.setLayout(new ColumnLayout());
		//mainContainer.setAutoHeight(true);
		//mainContainer.setAutoWidth(true);
		mainContainer.add(warnPersonPanel(),new com.extjs.gxt.ui.client.widget.layout.ColumnData(0.5));
		//mainContainer.add(new ContentPanel(),new com.extjs.gxt.ui.client.widget.layout.ColumnData(0.5));
		mainContainer.add(scriptPanel(),new com.extjs.gxt.ui.client.widget.layout.ColumnData(0.5));
		centerPanel.add(mainContainer);
		//centerPanel.add(warnPersonPanel());
		return centerPanel;
	}
	private FormPanel planPanel(){
		
		planPanel.setHeading("计划情况");
		FormData formData = new FormData("100%");  
		planPanel.setFrame(true);  
		planPanel.setWidth("100%");
		//planPanel.setSize(1050, -1);
		planPanel.add(actionTypeField);
		
		planNameField.setFieldLabel("计划名称");
		planNameField.setAllowBlank(false);
		
		remarkField.setFieldLabel("备注");
		
		FormLayout layout = new FormLayout();  
		layout.setLabelWidth(60);
		layout.setLabelAlign(LabelAlign.LEFT);  
		
		LayoutContainer columnOf2 = new LayoutContainer();
		columnOf2.setLayout(new ColumnLayout());
		
		LayoutContainer leftLayOut=new LayoutContainer();
		leftLayOut.setLayout(layout);
		//leftLayOut.setStyleAttribute("paddingRight", "2px");
		
		LayoutContainer rightLayOut=new LayoutContainer();
		layout = new FormLayout();  
		layout.setLabelWidth(60);
		layout.setLabelAlign(LabelAlign.LEFT); 
		rightLayOut.setLayout(layout);
		rightLayOut.setStyleAttribute("paddingLeft", "10px");
		
		
		leftLayOut.add(planNameField,formData);
		rightLayOut.add(remarkField,formData);
		columnOf2.add(leftLayOut,new com.extjs.gxt.ui.client.widget.layout.ColumnData(0.5));
		columnOf2.add(rightLayOut,new com.extjs.gxt.ui.client.widget.layout.ColumnData(0.5));
		
		LayoutContainer columnOf4 = new LayoutContainer();  
		columnOf4.setLayout(new ColumnLayout());  
		LayoutContainer column1 = new LayoutContainer();  
		column1.setStyleAttribute("paddingRight", "10px"); 
		layout = new FormLayout();  
		layout.setLabelWidth(60);
		layout.setLabelAlign(LabelAlign.LEFT); 
		column1.setLayout(layout);  
		LayoutContainer column2 = new LayoutContainer();  
		column2.setStyleAttribute("paddingLeft", "10px");  
		layout = new FormLayout();  
		layout.setLabelWidth(60);
		layout.setLabelAlign(LabelAlign.LEFT); 
	    column2.setLayout(layout);
	    LayoutContainer column3 = new LayoutContainer();  
		column3.setStyleAttribute("paddingLeft", "10px");  
		layout = new FormLayout();
		layout.setLabelWidth(60);
		layout.setLabelAlign(LabelAlign.LEFT); 
	    column3.setLayout(layout);
	    LayoutContainer column4 = new LayoutContainer();  
		column4.setStyleAttribute("paddingLeft", "10px");  
		layout = new FormLayout();
		layout.setLabelWidth(60);
		layout.setLabelAlign(LabelAlign.LEFT); 
	    column4.setLayout(layout);
	    
		String[] names=new String[]{"1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24"};
		
		beginHoursCombo.setFieldLabel("开始时段");
		beginHoursCombo.setDisplayField("name");
		beginHoursCombo.setStore(UiUtil.generateStore(names,names));
		beginHoursCombo.setTriggerAction(TriggerAction.ALL);
		beginHoursCombo.setEditable(false);
		beginHoursCombo.setAllowBlank(false);
		
		lasttTimeField.setFieldLabel("上次时间");
		
		
		runStsCombo.setFieldLabel("运行状态");
		runStsCombo.setDisplayField("name");
		runStsCombo.setStore(UiUtil.generateStore(new String[]{"运行","停止"},new String[]{"A","B"}));
		runStsCombo.setTriggerAction(TriggerAction.ALL);
		runStsCombo.setEditable(false);
		runStsCombo.setAllowBlank(false);
		
	    
	    endHoursCombo.setFieldLabel("结束时段");
	    endHoursCombo.setDisplayField("name");
	    endHoursCombo.setStore(UiUtil.generateStore(names,names));
	    endHoursCombo.setTriggerAction(TriggerAction.ALL);
	    endHoursCombo.setEditable(false);
	    endHoursCombo.setAllowBlank(false);
	    
	    nextTimeField.setFieldLabel("下次时间");
	    
	   
	    stsCombo.setFieldLabel("计划状态");
	    stsCombo.setDisplayField("name");
	    stsCombo.setStore(UiUtil.generateStore(new String[]{"运行","停止"},new String[]{"A","B"}));
	    stsCombo.setTriggerAction(TriggerAction.ALL);
	    stsCombo.setEditable(false);
	    stsCombo.setAllowBlank(false);
	    
	    planIdField.setFieldLabel("计划ID");
	    planIdField.setReadOnly(true);
	    planIdField.setToolTip("只读,新增时自动生成");
	    
	    companyIdField.setFieldLabel("公司ID");
	    companyIdField.setAllowBlank(false);
	    
	    areaCodeField.setFieldLabel("地区");
	    areaCodeField.setAllowBlank(false);
	    
	    dataTagField.setFieldLabel("数据标签");
	    dataTagField.setAllowBlank(false);
	    runCycleField.setFieldLabel("执行周期");
	    runCycleField.setAllowBlank(false);
	    runCycleField.setToolTip("分钟为单位");
	    runCycleField.setAllowBlank(false);
	    
	    column1.add(beginHoursCombo,formData);
	    column2.add(endHoursCombo,formData);
	    column3.add(lasttTimeField,formData);
	    column4.add(nextTimeField,formData);
	    column1.add(runCycleField,formData);
	    column2.add(runStsCombo,formData);
	    column3.add(stsCombo,formData);
	    column4.add(planIdField,formData);
	    
	    column1.add(companyIdField,formData);
	    column2.add(areaCodeField,formData);
	    column3.add(dataTagField,formData);
	    columnOf4.add(column1,new com.extjs.gxt.ui.client.widget.layout.ColumnData(0.25));
	    columnOf4.add(column2,new com.extjs.gxt.ui.client.widget.layout.ColumnData(0.25));
	    columnOf4.add(column3,new com.extjs.gxt.ui.client.widget.layout.ColumnData(0.25));
	    columnOf4.add(column4,new com.extjs.gxt.ui.client.widget.layout.ColumnData(0.25));
	    planPanel.add(columnOf2,formData);
	    planPanel.add(columnOf4,formData);
	    planPanel.setTopComponent(createPlanToolBar());
	    planPanel.setBodyBorder(true);
	    
		return planPanel;
	}
	
	private ToolBar createPlanToolBar(){
		Button createRecordButton=new Button("增加");
		createRecordButton.addSelectionListener(new SelectionListener<ButtonEvent>(){
			 public void componentSelected(ButtonEvent ce) {
				 isFormFieldReadOnly(false);
				 planPanel.reset();
				 companyIdField.setValue("1");
				 dataTagField.setValue("0591");
				 areaCodeField.setValue("0591");
				 actionTypeField.setValue("insert");
				 
				
			 }
		 });
		Button modifyRecordButton=new Button("修改");
		modifyRecordButton.addSelectionListener(new SelectionListener<ButtonEvent>(){
			 public void componentSelected(ButtonEvent ce) {
				 if(planIdField.getValue()==null){
					 MessageBox.alert("警告", "请选择需要修改的计划", null);
				 }else{
					 isFormFieldReadOnly(false);
					 actionTypeField.setValue("modify");
				 }
				
			 }
		 });
		Button deleteRecordButton=new Button("删除");
		deleteRecordButton.addSelectionListener(new SelectionListener<ButtonEvent>(){
			 public void componentSelected(ButtonEvent ce) {
				 if(planGrid.getSelectionModel().getSelectedItem()==null){
						MessageBox.alert("警告", "请选择需要删除的行", null);
						return; 
					}
					final ModelData modelData=planGrid.getSelectionModel().getSelectedItem();
					MessageBox.confirm("提示", "确认要删除<"+modelData.get("planName")+">吗?", new Listener<MessageBoxEvent>(){

						public void handleEvent(MessageBoxEvent be) {
							AsyncCallback deleteCallBack=new AsyncCallback(){
								public void onFailure(Throwable caught) {
									MessageBox.alert("alert",caught.getMessage(),null);
								}
								public void onSuccess(Object result) {
									if((Boolean)result){
										planGrid.getStore().remove(modelData);
										planPanel.reset();
									}else{
										MessageBox.info("提示","删除失败",null);
									}
								}
							};
							Map<String,String> inputParamMap=new HashMap<String,String>();
							inputParamMap.put("planId", (String)modelData.get("planId"));
							jsonRpc.request(GWT.getHostPageBaseURL()+ "scriptWarnAction/deleteScriptPlan.nut", inputParamMap, deleteCallBack);
							
						}
				
			 });
			 }
		 });
		Button comfirmRecordButton=new Button("确定");
		comfirmRecordButton.addSelectionListener(new SelectionListener<ButtonEvent>(){
			 public void componentSelected(ButtonEvent ce) {
				 if("insert".equals(actionTypeField.getValue()) && planPanel.isValid()){
					 final ModelData md=new BaseModelData();
					 transferFormFieldToModelData(md);
					 AsyncCallback insertCallBack=new AsyncCallback(){
							public void onFailure(Throwable caught) {
								MessageBox.alert("alert",caught.getMessage(),null);
							}
							public void onSuccess(Object result) {
								String planId=(String)result;
								md.set("planId", planId);//测试.
								planGrid.getStore().insert(md, 0);
								MessageBox.info("提示","插入成功",null);
							}
						};
					jsonRpc.requestStream(GWT.getHostPageBaseURL()+ "scriptWarnAction/insertScriptPlan.nut", md.getProperties(), insertCallBack);
					 
				 }else if("modify".equals(actionTypeField.getValue()) && planPanel.isValid()){
					 final ModelData md=planGrid.getSelectionModel().getSelectedItem();
					 transferFormFieldToModelData(md);
					 AsyncCallback updateCallBack=new AsyncCallback(){
							public void onFailure(Throwable caught) {
								MessageBox.alert("alert",caught.getMessage(),null);
							}
							public void onSuccess(Object result) {
								if((Boolean)result){
								planGrid.getStore().update(md);
								MessageBox.info("提示","更新成功",null);
								}else{
									MessageBox.info("提示","更新失败",null);
								}
							}
						};
					jsonRpc.requestStream(GWT.getHostPageBaseURL()+ "scriptWarnAction/updateScriptPlan.nut", md.getProperties(), updateCallBack);
					 
				 }
				
			 }
		 });
		Button copyRecordButton=new Button("复制");
		copyRecordButton.addSelectionListener(new SelectionListener<ButtonEvent>(){
			 public void componentSelected(ButtonEvent ce) {
				 if(planIdField.getValue()==null){
					 MessageBox.alert("警告", "请选择需要复制的计划", null);
				 }else{
					 ModelData willBeCopyModelData=planGrid.getSelectionModel().getSelectedItem();
					 final ModelData md=new BaseModelData();
					//获取新的一个ModelData。
						for (Iterator iterator = willBeCopyModelData.getPropertyNames().iterator(); iterator
								.hasNext();) {
							String name = (String) iterator.next();
							md.set(name, willBeCopyModelData.get(name));
						}

					 md.set("planId", "");
					 md.set("planName", (String)md.get("planName")+"_复制");
					 AsyncCallback copyCallBack=new AsyncCallback(){
							public void onFailure(Throwable caught) {
								MessageBox.alert("alert",caught.getMessage(),null);
							}
							public void onSuccess(Object result) {
								String planId=(String)result;
								 md.set("planId", planId);
								 planGrid.getStore().insert(md, 0);
							}
						};
					jsonRpc.requestStream(GWT.getHostPageBaseURL()+ "scriptWarnAction/insertScriptPlan.nut", md.getProperties(), copyCallBack);
					 
				 }
				
			 }
		 });
		ToolBar toolBar = new ToolBar();
	    toolBar.add(createRecordButton);
	    toolBar.add(new SeparatorToolItem());
	    toolBar.add(modifyRecordButton);
	    toolBar.add(new SeparatorToolItem());
	    toolBar.add(comfirmRecordButton);
	    toolBar.add(new SeparatorToolItem());
	    toolBar.add(deleteRecordButton);
	    toolBar.add(new SeparatorToolItem());
	    toolBar.add(copyRecordButton);
	    
	    return toolBar;
	}
	
	private ContentPanel scriptPanel(){
		ContentPanel scriptFromPanel=new ContentPanel();
		scriptFromPanel.setHeading("告警脚本");
		scriptArea.setWidth(400);
		scriptArea.setHeight(300);
		scriptFromPanel.add(scriptArea);
		Button createRecordButton=new Button("编辑");
		createRecordButton.addSelectionListener(new SelectionListener<ButtonEvent>(){
			@Override
			public void componentSelected(ButtonEvent ce) {
				scriptWarningScriptPopup.show();
			}
			
		});
		scriptWarningScriptPopup.setScriptContentTextArea(scriptArea);
		ToolBar toolBar = new ToolBar();
	    toolBar.add(createRecordButton);
	    scriptFromPanel.setTopComponent(toolBar);
		return scriptFromPanel;
	}

	private ContentPanel warnPersonPanel(){
		ContentPanel centerPanel=new ContentPanel();
		centerPanel.setHeading("告警联系人");
		ColumnConfig staffNameColumnConfig=new ColumnConfig("staffName", "姓名",50);
	    ColumnConfig staffNoColumnConfig=new ColumnConfig("staffNo", "工号", 75);
	    ColumnConfig telphoneColumnConfig=new ColumnConfig("connNbr", "电话号码",75);
	    ColumnConfig warnLevelColumnConfig=new ColumnConfig("warnLevel", "告警级别", 75);
	    ColumnConfig warnModelColumnConfig=new ColumnConfig("warnMode", "告警方式", 75);
	    ColumnConfig stsColumnConfig=new ColumnConfig("sts", "状态", 50);
	    stsColumnConfig.setRenderer(new GridCellRenderer<ModelData>(){

			public Object render(ModelData model, String property,
					ColumnData config, int rowIndex, int colIndex,
					ListStore<ModelData> store, Grid<ModelData> grid) {
				String sts=model.get("sts");
				if("A".equals(sts))
					return "在用";
				else
					return "不再用";
			}
	    	
	    });
	    warnModelColumnConfig.setRenderer(new GridCellRenderer<ModelData>(){
			public Object render(ModelData model, String property,
					ColumnData config, int rowIndex, int colIndex,
					ListStore<ModelData> store, Grid<ModelData> grid) {
				String warnMode=model.get("warnMode");
				if("1".equals(warnMode))
					return "软墙板";
				else if("2".equals(warnMode))
					return "短信";
				else if("3".equals(warnMode))
					return "语音";
				else if("4".equals(warnMode))
					return "Email";
				else
					return warnMode+"未知";
			}
	    });
	   
	    List<ColumnConfig> columns = new ArrayList<ColumnConfig>();  
	    columns.add(staffNameColumnConfig);
	    columns.add(staffNoColumnConfig);
	    columns.add(telphoneColumnConfig);
	    columns.add(warnLevelColumnConfig);
	    columns.add(warnModelColumnConfig);
	    columns.add(stsColumnConfig);
	    ColumnModel cm = new ColumnModel(columns);
		
		ModelType type = new ModelType();  
	    type.setRoot("records");
		type.addField("staffName", "staffName");
		type.addField("staffNo", "staffNo");
		type.addField("connNbr", "connNbr");
		type.addField("warnMode", "warnMode");
		type.addField("sts", "sts");
		type.addField("planId", "planId");
		type.addField("staffId", "staffId");
		String path =  GWT.getHostPageBaseURL()+ "scriptWarnAction/warnStaffList.nut";
	    RequestBuilder builder = new RequestBuilder(RequestBuilder.GET, path);  
	    HttpProxy<String> proxy = new HttpProxy<String>(builder); 
	    JsonLoadResultReader<ListLoadResult<ModelData>> reader=new JsonLoadResultReader<ListLoadResult<ModelData>>(type);
		final BaseListLoader<ListLoadResult<ModelData>> loader=new BaseListLoader<ListLoadResult<ModelData>>(proxy,reader); 
		final ListStore<ModelData> listStore=new ListStore<ModelData>(loader);
		
		final Grid<ModelData> warnStaffGrid = new Grid<ModelData>(listStore, cm);  
		Registry.register("PERSON_WARN_STORE", listStore);
		warnStaffGrid.setAutoExpandColumn("connNbr");
		warnStaffGrid.setHeight(304);
		
		centerPanel.add(warnStaffGrid);
		
		
		Button createRecordButton=new Button("增加");
		createRecordButton.addSelectionListener(new SelectionListener<ButtonEvent>(){
			@Override
			public void componentSelected(ButtonEvent ce) {
				scriptWarningPersonPopup.show();
			}
			
		});
		Button deleteRecordButton=new Button("删除");
		deleteRecordButton.addSelectionListener(new SelectionListener<ButtonEvent>(){

			@Override
			public void componentSelected(ButtonEvent ce) {
				final ModelData modelData;
				if(warnStaffGrid.getSelectionModel().getSelectedItem()==null){
					MessageBox.alert("警告", "请选择需要删除的行", null);
					return; 
				}
				modelData=warnStaffGrid.getSelectionModel().getSelectedItem();
				MessageBox.confirm("提示", "确认要删除<"+modelData.get("staffName")+">吗?", new Listener<MessageBoxEvent>(){

					public void handleEvent(MessageBoxEvent be) {
						if (!"Yes".equals(be.getButtonClicked().getText())){
							return ;
						}
						AsyncCallback deleteRecordCallBack=new AsyncCallback(){
							public void onFailure(Throwable caught) {
								MessageBox.alert("alert",caught.getMessage(),null);
							}
							public void onSuccess(Object result) {
								if((Boolean)result){
									warnStaffGrid.getStore().remove(modelData);
									MessageBox.info("提示", "删除成功", null);
								}else{
									MessageBox.info("提示","删除失败",null);
								}
								
							}
						};
						jsonRpc.request(GWT.getHostPageBaseURL()+ "scriptWarnAction/deleteWarnStaff.nut", modelData.getProperties(), deleteRecordCallBack);
						
					}
					
				});

				
			}
			
		});
		ToolBar toolBar = new ToolBar();
	    toolBar.add(createRecordButton);
	    toolBar.add(new SeparatorToolItem());
	    toolBar.add(deleteRecordButton);
	    centerPanel.setTopComponent(toolBar);
	    centerPanel.setStyleAttribute("paddingRight", "5px");
		
		return centerPanel;
	}
	
	private void transferFormFieldToModelData(ModelData md){
		md.set("planName", planNameField.getValue());
		md.set("areaCode", areaCodeField.getValue());
		md.set("planId", planIdField.getValue());
		md.set("companyId", companyIdField.getValue());
		md.set("remark", remarkField.getValue());
		md.set("runCycle", String.valueOf(runCycleField.getValue()));
		ModelData runStsMd=runStsCombo.getValue();
		md.set("runStatus", runStsMd.get("value"));
		md.set("lastTime", lasttTimeField.getValue());
		md.set("nextTime", nextTimeField.getValue());
		ModelData beginHoursMd=beginHoursCombo.getValue();
		md.set("beginHours", beginHoursMd.get("value"));
		ModelData endHoursMd=endHoursCombo.getValue();
		md.set("endHours", endHoursMd.get("value"));
		md.set("dataTagId", dataTagField.getValue());
		ModelData stsMd=stsCombo.getValue();
		md.set("sts", stsMd.get("value"));
		
	}
	
}
