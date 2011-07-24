package ecc.gwt.warning.client;

import java.util.ArrayList;
import java.util.List;
import java.util.logging.Logger;

import com.extjs.gxt.ui.client.Registry;
import com.extjs.gxt.ui.client.Style.LayoutRegion;
import com.extjs.gxt.ui.client.data.BaseModelData;
import com.extjs.gxt.ui.client.data.ModelData;
import com.extjs.gxt.ui.client.event.ButtonEvent;
import com.extjs.gxt.ui.client.event.SelectionListener;
import com.extjs.gxt.ui.client.store.ListStore;
import com.extjs.gxt.ui.client.util.Margins;
import com.extjs.gxt.ui.client.widget.ContentPanel;
import com.extjs.gxt.ui.client.widget.LayoutContainer;
import com.extjs.gxt.ui.client.widget.Popup;
import com.extjs.gxt.ui.client.widget.Window;
import com.extjs.gxt.ui.client.widget.button.Button;
import com.extjs.gxt.ui.client.widget.form.ComboBox;
import com.extjs.gxt.ui.client.widget.form.FormPanel;
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
import com.google.gwt.user.client.Element;
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
	public ScriptWarnConfigPanel(){
		logger=Logger.getLogger("ecc.gwt.warning.client.ScriptWarnConfigPanel");
		BorderLayout borderLayout=new BorderLayout();
		setLayout(borderLayout);
		planGrid=generatePlanGrid();
		scriptWarningPersonPopup=new ScriptWarningPersonPopup();
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
		westLayoutData.setMargins(new Margins(5));
		BorderLayoutData centerLayoutData=new BorderLayoutData(LayoutRegion.CENTER);
		add(westPanel,westLayoutData);
	    centerLayoutData.setMargins(new Margins(5));
	    add(centerPanel(),centerLayoutData);
	    
	}
	
	private Grid<ModelData> generatePlanGrid(){
		ColumnConfig planNameColumnConfig=new ColumnConfig("planName", "计划名称",130);
	    ColumnConfig runStsColumnConfig=new ColumnConfig("runSts", "运行状态", 70);
	    runStsColumnConfig.setRenderer(new GridCellRenderer<ModelData>(){
			public Object render(ModelData model, String property,
					ColumnData config, int rowIndex, int colIndex,
					ListStore<ModelData> store, Grid<ModelData> grid) {
				String sts=model.get("runSts");
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
	    
		String[] names={"催缴告警计划2","催缴是否开启监控"};
		String[] values={"1","2"};
		//ListStore<ModelData> listStore=UiUtil.generateStore(names, values);
		ListStore<ModelData> listStore=new ListStore<ModelData>();
		ModelData modelData1=new BaseModelData();
		modelData1.set("planName", "催缴告警计划2");
		modelData1.set("runSts", "A");
		ModelData modelData2=new BaseModelData();
		modelData2.set("planName", "催缴是否开启监控");
		modelData2.set("runSts", "A");
		listStore.add(modelData1);
		listStore.add(modelData2);
		Grid<ModelData> grid = new Grid<ModelData>(listStore, cm);  
		grid.setHeight(470);
		grid.setAutoWidth(true);
		return grid;
		
	}
	
	private ContentPanel centerPanel(){
		ContentPanel centerPanel=new ContentPanel();
		centerPanel.setHeaderVisible(false);
		//centerPanel.add(createColumnForm());
		centerPanel.add(planPanel());
		LayoutContainer mainContainer=new LayoutContainer();
		mainContainer.setLayout(new ColumnLayout());
		mainContainer.setAutoHeight(true);
		mainContainer.setAutoWidth(true);
		mainContainer.add(warnPersonPanel(),new com.extjs.gxt.ui.client.widget.layout.ColumnData(0.5));
		mainContainer.add(scriptPanel(),new com.extjs.gxt.ui.client.widget.layout.ColumnData(0.5));
		centerPanel.add(mainContainer);
		//centerPanel.add(warnPersonPanel());
		return centerPanel;
	}
	private ContentPanel planPanel(){
		ContentPanel planPanel=new FormPanel();
		planPanel.setHeading("计划情况");
		FormData formData = new FormData("100%");  
		planPanel.setFrame(true);  
		planPanel.setSize(1050, -1);
		
		final TextField<String> planNameField=new TextField<String>();
		planNameField.setFieldLabel("计划名称");
		final TextField<String> remarkField=new TextField<String>();
		remarkField.setFieldLabel("备注");
		
		FormLayout layout = new FormLayout();  
		layout.setLabelAlign(LabelAlign.LEFT);  
		
		LayoutContainer columnOf2 = new LayoutContainer();
		columnOf2.setLayout(new ColumnLayout());
		
		LayoutContainer leftLayOut=new LayoutContainer();
		leftLayOut.setLayout(layout);
		leftLayOut.setStyleAttribute("paddingRight", "10px");
		
		LayoutContainer rightLayOut=new LayoutContainer();
		layout = new FormLayout();  
		layout.setLabelAlign(LabelAlign.LEFT); 
		rightLayOut.setLayout(layout);
		rightLayOut.setStyleAttribute("paddingRight", "10px");
		
		
		leftLayOut.add(planNameField,formData);
		rightLayOut.add(remarkField,formData);
		columnOf2.add(leftLayOut,new com.extjs.gxt.ui.client.widget.layout.ColumnData(0.5));
		columnOf2.add(rightLayOut,new com.extjs.gxt.ui.client.widget.layout.ColumnData(0.5));
		
		LayoutContainer columnOf4 = new LayoutContainer();  
		columnOf4.setLayout(new ColumnLayout());  
		LayoutContainer column1 = new LayoutContainer();  
		column1.setStyleAttribute("paddingRight", "10px"); 
		layout = new FormLayout();  
		layout.setLabelAlign(LabelAlign.LEFT); 
		column1.setLayout(layout);  
		LayoutContainer column2 = new LayoutContainer();  
		column2.setStyleAttribute("paddingLeft", "10px");  
		layout = new FormLayout();  
		layout.setLabelAlign(LabelAlign.LEFT); 
	    column2.setLayout(layout);
	    LayoutContainer column3 = new LayoutContainer();  
		column3.setStyleAttribute("paddingLeft", "10px");  
		layout = new FormLayout();  
		layout.setLabelAlign(LabelAlign.LEFT); 
	    column3.setLayout(layout);
	    LayoutContainer column4 = new LayoutContainer();  
		column4.setStyleAttribute("paddingLeft", "10px");  
		layout = new FormLayout();  
		layout.setLabelAlign(LabelAlign.LEFT); 
	    column4.setLayout(layout);
	    
		String[] names=new String[]{"1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24"};
		final ComboBox<ModelData> startHourCombo = new ComboBox<ModelData>();
		startHourCombo.setFieldLabel("开始时段");
		startHourCombo.setDisplayField("name");
		startHourCombo.setStore(UiUtil.generateStore(names,names));
		startHourCombo.setTriggerAction(TriggerAction.ALL);
		startHourCombo.setEditable(false);
		final TextField<String> lastExecTimeField=new TextField<String>();
		lastExecTimeField.setFieldLabel("上次时间");
		
		final ComboBox<ModelData> runStsCombo = new ComboBox<ModelData>();
		runStsCombo.setFieldLabel("运行状态");
		runStsCombo.setDisplayField("name");
		runStsCombo.setStore(UiUtil.generateStore(new String[]{"运行","停止"},new String[]{"A","B"}));
		runStsCombo.setTriggerAction(TriggerAction.ALL);
		runStsCombo.setEditable(false);
		
	    final ComboBox<ModelData> endHourCombo = new ComboBox<ModelData>();
	    endHourCombo.setFieldLabel("结束时段");
	    endHourCombo.setDisplayField("name");
	    endHourCombo.setStore(UiUtil.generateStore(names,names));
	    endHourCombo.setTriggerAction(TriggerAction.ALL);
	    endHourCombo.setEditable(false);
	    final TextField<String> nextExecTimeField=new TextField<String>();
	    nextExecTimeField.setFieldLabel("下次时间");
	    
	    final ComboBox<ModelData> stsCombo = new ComboBox<ModelData>();
	    stsCombo.setFieldLabel("计划状态");
	    stsCombo.setDisplayField("name");
	    stsCombo.setStore(UiUtil.generateStore(new String[]{"运行","停止"},new String[]{"A","B"}));
	    stsCombo.setTriggerAction(TriggerAction.ALL);
	    stsCombo.setEditable(false);
	    final TextField<String> planIdField=new TextField<String>();
	    planIdField.setFieldLabel("计划ID");
	    final TextField<String> companyIdField=new TextField<String>();
	    companyIdField.setFieldLabel("公司ID");
	    final TextField<String> areaCodeField=new TextField<String>();
	    areaCodeField.setFieldLabel("地区");
	    final TextField<String> dataTagField=new TextField<String>();
	    dataTagField.setFieldLabel("数据标签");
	    
	    column1.add(startHourCombo,formData);
	    column2.add(endHourCombo,formData);
	    column3.add(lastExecTimeField,formData);
	    column4.add(nextExecTimeField,formData);
	    column1.add(planIdField,formData);
	    column2.add(companyIdField,formData);
	    column3.add(areaCodeField,formData);
	    column4.add(dataTagField,formData);
	    columnOf4.add(column1,new com.extjs.gxt.ui.client.widget.layout.ColumnData(0.25));
	    columnOf4.add(column2,new com.extjs.gxt.ui.client.widget.layout.ColumnData(0.25));
	    columnOf4.add(column3,new com.extjs.gxt.ui.client.widget.layout.ColumnData(0.25));
	    columnOf4.add(column4,new com.extjs.gxt.ui.client.widget.layout.ColumnData(0.25));
	    planPanel.add(columnOf2,formData);
	    planPanel.add(columnOf4,formData);
	    planPanel.setTopComponent(createPlanToolBar());
	    
		return planPanel;
	}
	
	private ToolBar createPlanToolBar(){
		Button createRecordButton=new Button("增加");
		Button modifyRecordButton=new Button("修改");
		Button deleteRecordButton=new Button("删除");
		Button comfirmRecordButton=new Button("确定");
		Button copyRecordButton=new Button("复制");
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
		final TextArea scriptArea=new TextArea();
		scriptArea.setWidth(500);
		scriptArea.setHeight(300);
		scriptFromPanel.add(scriptArea);
		Button createRecordButton=new Button("增加");
		Button modifyRecordButton=new Button("修改");
		Button comfirmRecordButton=new Button("确定");
		ToolBar toolBar = new ToolBar();
	    toolBar.add(createRecordButton);
	    toolBar.add(new SeparatorToolItem());
	    toolBar.add(modifyRecordButton);
	    toolBar.add(new SeparatorToolItem());
	    toolBar.add(comfirmRecordButton);
	    scriptFromPanel.setTopComponent(toolBar);
		return scriptFromPanel;
	}

	private ContentPanel warnPersonPanel(){
		ContentPanel centerPanel=new ContentPanel();
		centerPanel.setHeading("告警联系人");
		ColumnConfig staffNameColumnConfig=new ColumnConfig("staffName", "姓名",100);
	    ColumnConfig staffNoColumnConfig=new ColumnConfig("staffNo", "工号", 100);
	    ColumnConfig telphoneColumnConfig=new ColumnConfig("telPhone", "电话号码",100);
	    ColumnConfig warnLevelColumnConfig=new ColumnConfig("warnLevel", "告警级别", 100);
	    ColumnConfig warnModelColumnConfig=new ColumnConfig("warnModel", "告警方式", 100);
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
					return "未知";
			}
	    });
	   
	    List<ColumnConfig> columns = new ArrayList<ColumnConfig>();  
	    columns.add(staffNameColumnConfig);
	    columns.add(staffNoColumnConfig);
	    columns.add(telphoneColumnConfig);
	    columns.add(warnLevelColumnConfig);
	    columns.add(warnModelColumnConfig);
	    ColumnModel cm = new ColumnModel(columns);
	    ListStore<ModelData> listStore=new ListStore<ModelData>();
		ModelData modelData1=new BaseModelData();
		modelData1.set("staffName", "A");
		modelData1.set("staffNo", "591123426");
		modelData1.set("telPhone", "18959130026");
		modelData1.set("warnLevel", "A");
		modelData1.set("warnMode", "2");
		listStore.add(modelData1);
		Grid<ModelData> grid = new Grid<ModelData>(listStore, cm);  
		Registry.register("PERSON_WARN_STORE", listStore);
		grid.setHeight(300);
		grid.setAutoWidth(true);
		centerPanel.setAutoHeight(true);
		centerPanel.setAutoWidth(true);
		centerPanel.add(grid);
		
		
		Button createRecordButton=new Button("增加");
		createRecordButton.addSelectionListener(new SelectionListener<ButtonEvent>(){
			@Override
			public void componentSelected(ButtonEvent ce) {
				scriptWarningPersonPopup.show();
			}
			
		});
		Button deleteRecordButton=new Button("删除");
		ToolBar toolBar = new ToolBar();
	    toolBar.add(createRecordButton);
	    toolBar.add(new SeparatorToolItem());
	    toolBar.add(deleteRecordButton);
	    centerPanel.setTopComponent(toolBar);
	    centerPanel.setStyleAttribute("paddingRight", "20px");
		
		return centerPanel;
	}
	
}
