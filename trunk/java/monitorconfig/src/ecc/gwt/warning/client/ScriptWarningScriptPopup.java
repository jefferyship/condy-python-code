package ecc.gwt.warning.client;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.logging.Logger;

import com.extjs.gxt.ui.client.Style.HorizontalAlignment;
import com.extjs.gxt.ui.client.data.BaseListLoader;
import com.extjs.gxt.ui.client.data.BaseModelData;
import com.extjs.gxt.ui.client.data.HttpProxy;
import com.extjs.gxt.ui.client.data.JsonLoadResultReader;
import com.extjs.gxt.ui.client.data.ListLoadResult;
import com.extjs.gxt.ui.client.data.ModelData;
import com.extjs.gxt.ui.client.data.ModelType;
import com.extjs.gxt.ui.client.event.ButtonEvent;
import com.extjs.gxt.ui.client.event.Events;
import com.extjs.gxt.ui.client.event.GridEvent;
import com.extjs.gxt.ui.client.event.Listener;
import com.extjs.gxt.ui.client.event.SelectionListener;
import com.extjs.gxt.ui.client.store.ListStore;
import com.extjs.gxt.ui.client.widget.ContentPanel;
import com.extjs.gxt.ui.client.widget.MessageBox;
import com.extjs.gxt.ui.client.widget.Window;
import com.extjs.gxt.ui.client.widget.button.Button;
import com.extjs.gxt.ui.client.widget.form.FormPanel;
import com.extjs.gxt.ui.client.widget.form.HiddenField;
import com.extjs.gxt.ui.client.widget.form.TextArea;
import com.extjs.gxt.ui.client.widget.form.TextField;
import com.extjs.gxt.ui.client.widget.grid.ColumnConfig;
import com.extjs.gxt.ui.client.widget.grid.ColumnModel;
import com.extjs.gxt.ui.client.widget.grid.Grid;
import com.extjs.gxt.ui.client.widget.grid.RowNumberer;
import com.extjs.gxt.ui.client.widget.layout.ColumnLayout;
import com.google.gwt.core.client.GWT;
import com.google.gwt.http.client.RequestBuilder;
import com.google.gwt.user.client.Element;
import com.google.gwt.user.client.rpc.AsyncCallback;

public class ScriptWarningScriptPopup extends Window {
	private final HiddenField<String> scriptId=new HiddenField<String>();
	private final HiddenField<String> actionType=new HiddenField<String>();
	private final TextField<String> scriptRemark=new TextField<String>();
	private final TextArea scriptContent=new TextArea();
	private final Grid<ModelData> grid;
	private final Grid<ModelData> planGrid;
	final private JsonRpc jsonRpc=new JsonRpc();
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
	    ModelType type = new ModelType();  
	    type.setRoot("records");
		type.addField("scriptId", "scriptId");
		type.addField("scriptRemark", "scriptRemark");
		type.addField("scriptbash", "scriptbash");
		type.addField("sts", "sts");
		String path =  GWT.getHostPageBaseURL()+ "scriptWarnAction/listWarnScript.nut";
	    RequestBuilder builder = new RequestBuilder(RequestBuilder.GET, path);  
	    HttpProxy<String> proxy = new HttpProxy<String>(builder); 
	    JsonLoadResultReader<ListLoadResult<ModelData>> reader=new JsonLoadResultReader<ListLoadResult<ModelData>>(type);
		final BaseListLoader<ListLoadResult<ModelData>> loader=new BaseListLoader<ListLoadResult<ModelData>>(proxy,reader); 
		final ListStore<ModelData> listStore=new ListStore<ModelData>(loader);
		final Grid<ModelData> grid = new Grid<ModelData>(listStore, cm);  
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
	    grid.setLoadMask(true);  
	    loader.load();
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
				 if("insert".equals(actionType.getValue()) && formPanel.isValid()){
					 scriptRemark.setReadOnly(true);
					 scriptContent.setReadOnly(true);
					 final ModelData newModelData=new BaseModelData();
					 newModelData.set("scriptId", scriptId.getValue());
					 newModelData.set("scriptRemark", scriptRemark.getValue());
					 newModelData.set("scriptbash", scriptContent.getValue());
					 newModelData.set("sts", "A");
					 AsyncCallback insertCallBack=new AsyncCallback(){
							public void onFailure(Throwable caught) {
								MessageBox.alert("alert",caught.getMessage(),null);
							}
							public void onSuccess(Object result) {
								newModelData.set("scriptId", result);
								grid.getStore().insert(newModelData, 0);
								MessageBox.info("提示", "新增成功", null);
								
							}
						};
						jsonRpc.requestStream(GWT.getHostPageBaseURL()+ "scriptWarnAction/insertWarnScript.nut", newModelData.getProperties(), insertCallBack);
					 
						
					 
				 }else if ("modify".equals(actionType.getValue())&& formPanel.isValid()){
					 final ModelData currModelData=grid.getSelectionModel().getSelectedItem();
					 currModelData.set("scriptRemark", scriptRemark.getValue());
					 currModelData.set("scriptbash", scriptContent.getValue());
					 AsyncCallback modifyCallBack=new AsyncCallback(){
							public void onFailure(Throwable caught) {
								MessageBox.alert("alert",caught.getMessage(),null);
							}
							public void onSuccess(Object result) {
								if((Boolean)result){
									grid.getStore().update(currModelData);
									scriptRemark.setReadOnly(true);
									scriptContent.setReadOnly(true);
									MessageBox.info("提示", "修改成功", null);
								}else{
									MessageBox.info("提示","修改失败",null);
								}
							}
						};
					 jsonRpc.requestStream(GWT.getHostPageBaseURL()+ "scriptWarnAction/updateWarnScript.nut", currModelData.getProperties(), modifyCallBack);
					 
				 }
				 
			 }
		 });
		 Button checkRecordButton=new Button("选中");
		 checkRecordButton.addSelectionListener(new SelectionListener<ButtonEvent>(){
			@Override
			public void componentSelected(ButtonEvent ce) {
				if(grid.getSelectionModel().getSelectedItem()==null){
					MessageBox.alert("提示", "请选择选中的行", null);
				}else if (planGrid.getSelectionModel().getSelectedItem()==null){
					MessageBox.alert("提示", "请在计划列表中选择需要选中的计划", null);
				}else{
					final ModelData currModelData=grid.getSelectionModel().getSelectedItem();
					//更新scrptId,到计划grid选中的modelData中.
					final ModelData planModelData=planGrid.getSelectionModel().getSelectedItem();
					AsyncCallback confirmCallBack=new AsyncCallback(){
						public void onFailure(Throwable caught) {
							MessageBox.alert("alert",caught.getMessage(),null);
						}
						public void onSuccess(Object result) {
							if((Boolean)result){
								planModelData.set("scriptId", currModelData.get("scriptId"));
								planGrid.getStore().update(planModelData);
								//更新scriptContent到textarea中.
								scriptContentTextArea.setValue((String)currModelData.get("scriptbash"));
								formPanel.reset();
								hide();
							}else{
								MessageBox.info("提示","选择失败",null);
							}
						}
					};
					Map<String,String> inputParamMap=new HashMap<String,String>();
					inputParamMap.put("planId", (String)planModelData.get("planId"));
					inputParamMap.put("scriptId", (String)currModelData.get("scriptId"));
				    jsonRpc.request(GWT.getHostPageBaseURL()+ "scriptWarnAction/planConfirmWarnScript.nut", inputParamMap, confirmCallBack);
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
