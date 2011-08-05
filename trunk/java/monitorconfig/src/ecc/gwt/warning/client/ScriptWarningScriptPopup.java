package ecc.gwt.warning.client;

import java.util.ArrayList;
import java.util.List;
import java.util.logging.Logger;

import com.extjs.gxt.ui.client.Style.HorizontalAlignment;
import com.extjs.gxt.ui.client.data.BaseModelData;
import com.extjs.gxt.ui.client.data.ModelData;
import com.extjs.gxt.ui.client.event.ButtonEvent;
import com.extjs.gxt.ui.client.event.Events;
import com.extjs.gxt.ui.client.event.GridEvent;
import com.extjs.gxt.ui.client.event.Listener;
import com.extjs.gxt.ui.client.event.SelectionListener;
import com.extjs.gxt.ui.client.store.ListStore;
import com.extjs.gxt.ui.client.widget.ContentPanel;
import com.extjs.gxt.ui.client.widget.Dialog;
import com.extjs.gxt.ui.client.widget.MessageBox;
import com.extjs.gxt.ui.client.widget.Window;
import com.extjs.gxt.ui.client.widget.button.Button;
import com.extjs.gxt.ui.client.widget.form.FormPanel;
import com.extjs.gxt.ui.client.widget.form.HiddenField;
import com.extjs.gxt.ui.client.widget.form.TextArea;
import com.extjs.gxt.ui.client.widget.form.TextField;
import com.extjs.gxt.ui.client.widget.grid.CheckBoxSelectionModel;
import com.extjs.gxt.ui.client.widget.grid.CheckColumnConfig;
import com.extjs.gxt.ui.client.widget.grid.ColumnConfig;
import com.extjs.gxt.ui.client.widget.grid.ColumnModel;
import com.extjs.gxt.ui.client.widget.grid.Grid;
import com.extjs.gxt.ui.client.widget.grid.RowNumberer;
import com.extjs.gxt.ui.client.widget.layout.ColumnLayout;
import com.google.gwt.user.client.Element;
import com.telthink.iserv.util.Log;

public class ScriptWarningScriptPopup extends Window {
	private final HiddenField<String> scriptId=new HiddenField<String>();
	private final HiddenField<String> actionType=new HiddenField<String>();
	private final TextField<String> scriptRemark=new TextField<String>();
	private final TextArea scriptContent=new TextArea();
	private final Grid<ModelData> grid;
	private final Grid<ModelData> planGrid;
	private TextArea scriptContentTextArea;//从ScriptWarnConfigPanel的scriptPanel方法将对象设置到本类中.
	
	
	private Logger logger;
	public ScriptWarningScriptPopup(Grid<ModelData> planGrid){
		logger=Logger.getLogger("ecc.gwt.warning.client.ScriptWarnConfigPanel");
		setSize(450, 230);
		setBorders(true);
		setShadow(false);
		setAutoHide(false);
		setTitle("脚本策略");
		this.planGrid=planGrid;
		grid=createScriptGrid();
		
	}
	
	
	public TextArea getScriptContentTextArea() {
		return scriptContentTextArea;
	}


	public void setScriptContentTextArea(TextArea scriptContentTextArea) {
		this.scriptContentTextArea = scriptContentTextArea;
	}


	protected void onRender(Element target, int index) {
		super.onRender(target, index);
		setLayout(new ColumnLayout());
		ContentPanel centerPanel=new ContentPanel();centerPanel.setHeaderVisible(false);
		centerPanel.setAutoHeight(true);
		centerPanel.setAutoWidth(true);
		centerPanel.add(grid);
		add(centerPanel,new com.extjs.gxt.ui.client.widget.layout.ColumnData(0.3));
		add(createScriptFormPanel(),new com.extjs.gxt.ui.client.widget.layout.ColumnData(0.7));
	}
	private Grid<ModelData> createScriptGrid(){
		
		ColumnConfig scriptIdColumnConfig=new ColumnConfig("scriptId", "id",30);
	    ColumnConfig scriptRemarkColumnConfig=new ColumnConfig("scriptRemark", "名称", 75);
	    List<ColumnConfig> columns = new ArrayList<ColumnConfig>(); 
	    columns.add(new RowNumberer());
	    columns.add(scriptRemarkColumnConfig);
	    columns.add(scriptIdColumnConfig);
	    ColumnModel cm = new ColumnModel(columns);
	    ListStore<ModelData> listStore=new ListStore<ModelData>();
		ModelData modelData1=new BaseModelData();
		modelData1.set("scriptId", "1");
		modelData1.set("scriptRemark", "aaaaaaaa");
		modelData1.set("scriptbash", "aaaaaaaa");
		listStore.add(modelData1);
		final Grid<ModelData> grid = new Grid<ModelData>(listStore, cm);  
		//grid.setSelectionModel(new CheckBoxSelectionModel<ModelData>());
		grid.addListener(Events.RowClick, new Listener<GridEvent<ModelData>>(){
			public void handleEvent(GridEvent<ModelData> be) {
				ModelData md=be.getModel();
				scriptRemark.setReadOnly(true);
				scriptContent.setReadOnly(true);
				scriptId.setValue((String)md.get("scriptId"));
				scriptRemark.setValue((String)md.get("scriptRemark"));
				scriptContent.setValue((String)md.get("scriptbash"));
			}
			
		});
		grid.setHeight(150);
		grid.setAutoWidth(true);
		
		return grid;
	}
	
	private FormPanel createScriptFormPanel(){
		 final FormPanel formPanel=new FormPanel();
		 scriptRemark.setAllowBlank(false);
		 scriptRemark.setFieldLabel("名称");
		 scriptRemark.setReadOnly(true);
		 scriptContent.setAllowBlank(true);
		 scriptContent.setFieldLabel("脚本");
		 scriptContent.setReadOnly(true);
		 scriptContent.setHeight(100);
		 formPanel.add(actionType);
		 formPanel.add(scriptId);
		 formPanel.add(scriptRemark);
		 formPanel.add(scriptContent);
		 formPanel.setHeaderVisible(false);
		 formPanel.setButtonAlign(HorizontalAlignment.CENTER);
		 Button createRecordButton=new Button("新增");
		 createRecordButton.setWidth(40);
		 createRecordButton.addSelectionListener(new SelectionListener<ButtonEvent>(){
			 public void componentSelected(ButtonEvent ce) {
				 //@TODO 从数据库中获取scriptId值.
				 formPanel.reset();
				 scriptRemark.setReadOnly(false);
				 scriptContent.setReadOnly(false);
				 actionType.setValue("insert");
			 }
		 });
		 Button modifyRecordButton=new Button("修改");
		 
		 modifyRecordButton.setWidth(40);
		 modifyRecordButton.addSelectionListener(new SelectionListener<ButtonEvent>(){
			 public void componentSelected(ButtonEvent ce) {
				 scriptRemark.setReadOnly(false);
				 scriptContent.setReadOnly(false);
				 actionType.setValue("modify");
			 }
		 });
		 Button comfirmRecordButton=new Button("确定");
		 comfirmRecordButton.setWidth(40);
		 comfirmRecordButton.addSelectionListener(new SelectionListener<ButtonEvent>(){
			 public void componentSelected(ButtonEvent ce) {
				 //@TODO 从数据库中获取脚本策略scriptId值.
				 if("insert".equals(actionType.getValue()) && formPanel.isValid()){
					 //@TODO  将脚本策略插入数据库中.
					 scriptRemark.setReadOnly(true);
					 scriptContent.setReadOnly(true);
					 ModelData newModelData=new BaseModelData();
					 newModelData.set("scriptId", scriptId.getValue());
					 newModelData.set("scriptRemark", scriptRemark.getValue());
					 newModelData.set("content", scriptContent.getValue());
					 newModelData.set("sts", "A");
					 grid.getStore().insert(newModelData, 0);
					 
				 }else if ("modify".equals(actionType.getValue())&& formPanel.isValid()){
					//@TODO  将脚本策略更新数据库中.
					 ModelData currModelData=grid.getStore().findModel("scriptId", "1");
					 //odelData currModelData=grid.getSelectionModel().getSelectedItem();
					 logger.info("test:"+(String)currModelData.get("scriptId"));
					 currModelData.set("scriptRemark", scriptRemark.getValue());
					 currModelData.set("scriptbash", scriptContent.getValue());
					 logger.info("test:"+(String)currModelData.get("scriptRemark"));
					 grid.getStore().update(currModelData);
					 scriptRemark.setReadOnly(true);
					 scriptContent.setReadOnly(true);
				 }
				 
			 }
		 });
		 Button checkRecordButton=new Button("选中");
		 checkRecordButton.addSelectionListener(new SelectionListener<ButtonEvent>(){
			@Override
			public void componentSelected(ButtonEvent ce) {
				logger.info("test:");
				logger.info("test:"+grid.getSelectionModel());
				if(grid.getSelectionModel().getSelectedItem()!=null){
					ModelData currModelData=grid.getSelectionModel().getSelectedItem();
					//@TODO 更新到数据库中.
					
					//更新scrptId,到计划grid选中的modelData中.
					/*ModelData planModelData=planGrid.getSelectionModel().getSelectedItem();
					planModelData.set("scriptId", currModelData.get("scriptId"));
					planGrid.getStore().update(planModelData);*/
					
					//更新scriptContent到textarea中.
					scriptContentTextArea.setValue((String)currModelData.get("scriptbash"));
					formPanel.reset();
					hide();
					
				}else{
					MessageBox.alert("提示", "请选择选中的行", null);
				}
			}
			
		});
		 checkRecordButton.setWidth(40);
		 formPanel.addButton(createRecordButton);
		 formPanel.addButton(modifyRecordButton);
		 formPanel.addButton(comfirmRecordButton);
		 formPanel.addButton(checkRecordButton);
		 
		 
		return formPanel;
	}

}
