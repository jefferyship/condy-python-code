package ecc.gwt.warning.client;


import java.util.HashMap;
import java.util.Map;
import java.util.logging.Logger;

import com.extjs.gxt.ui.client.Registry;
import com.extjs.gxt.ui.client.Style.HorizontalAlignment;
import com.extjs.gxt.ui.client.data.BaseModelData;
import com.extjs.gxt.ui.client.data.ModelData;
import com.extjs.gxt.ui.client.event.ButtonEvent;
import com.extjs.gxt.ui.client.event.ComponentEvent;
import com.extjs.gxt.ui.client.event.KeyListener;
import com.extjs.gxt.ui.client.event.SelectionListener;
import com.extjs.gxt.ui.client.store.ListStore;
import com.extjs.gxt.ui.client.widget.MessageBox;
import com.extjs.gxt.ui.client.widget.Window;
import com.extjs.gxt.ui.client.widget.button.Button;
import com.extjs.gxt.ui.client.widget.form.ComboBox;
import com.extjs.gxt.ui.client.widget.form.FormPanel;
import com.extjs.gxt.ui.client.widget.form.HiddenField;
import com.extjs.gxt.ui.client.widget.form.TextField;
import com.extjs.gxt.ui.client.widget.form.ComboBox.TriggerAction;
import com.extjs.gxt.ui.client.widget.grid.Grid;
import com.extjs.gxt.ui.client.widget.layout.FitLayout;
import com.google.gwt.core.client.GWT;
import com.google.gwt.event.dom.client.KeyCodes;
import com.google.gwt.user.client.Element;
import com.google.gwt.user.client.rpc.AsyncCallback;

public class ScriptWarningPersonPopup extends Window {
	private final HiddenField<String> staffId=new HiddenField<String>();
	private final ComboBox<ModelData> stsCombo=new ComboBox<ModelData>();
	private final HiddenField<String> actionType=new HiddenField<String>();
	private final TextField<String> staffNo=new TextField<String>();
	private final TextField<String> staffName=new TextField<String>();
	private final TextField<String> telPhone=new TextField<String>();
	private final TextField<String> email=new TextField<String>();
	private final ComboBox<ModelData> warnLevelCombo = new ComboBox<ModelData>();
	private final ComboBox<ModelData> warnModelCombo = new ComboBox<ModelData>();
	private final Grid<ModelData> planGrid;
	private Logger logger;
    final FormPanel formPanel=new FormPanel();
	final private JsonRpc jsonRpc=new JsonRpc();
	
	void setFormFied(String actionType,ModelData modelData){
		this.actionType.setValue(actionType);
		if("insert".equals(actionType)){
			staffId.setReadOnly(false);
			staffNo.setReadOnly(false);
			staffName.setReadOnly(false);
			stsCombo.setValue(stsCombo.getStore().findModel("value", "A"));
			warnLevelCombo.setValue(warnLevelCombo.getStore().findModel("value", "A"));
			warnModelCombo.setValue(warnModelCombo.getStore().findModel("name", "短信"));
		}else if("modify".equals(actionType)){
		staffId.setValue((String)modelData.get("staffId"));
		logger.info((String)modelData.get("sts"));
		logger.info(String.valueOf(stsCombo.getStore().findModel("value", (String)modelData.get("sts"))));
		stsCombo.setValue(stsCombo.getStore().findModel("value", (String)modelData.get("sts")));
		staffNo.setValue((String)modelData.get("staffNo"));
		staffName.setValue((String)modelData.get("staffName"));
		telPhone.setValue((String)modelData.get("connNbr"));
		email.setValue((String)modelData.get("email"));
		warnLevelCombo.setValue(warnLevelCombo.getStore().findModel("value", (String)modelData.get("warnLevel")));
		warnModelCombo.setValue(warnModelCombo.getStore().findModel("value", (String)modelData.get("warnMode")));
		staffId.setReadOnly(true);
		staffNo.setReadOnly(true);
		staffName.setReadOnly(true);
		}
		
	}

	public ScriptWarningPersonPopup(Grid<ModelData> planGrid){
		logger=Logger.getLogger("ecc.gwt.warning.client.ScriptWarnConfigPanel");
		this.planGrid=planGrid;
		setSize(350, 270);
		setBorders(true);
		setShadow(false);
		setAutoHide(false);
		setTitle("告警联系人");
	}

	/* (non-Javadoc)
	 * @see com.extjs.gxt.ui.client.widget.Popup#onRender(com.google.gwt.user.client.Element, int)
	 */
	@Override
	protected void onRender(Element target, int index) {
		super.onRender(target, index);
		setLayout(new FitLayout());
		
		add(ceateFormPanel());
	}
	
	private FormPanel ceateFormPanel(){
		
		staffNo.setAllowBlank(false);
		staffNo.setFieldLabel("工号");
		staffNo.setToolTip("输入9位工号,并且回车");
		
		
		staffName.setAllowBlank(false);	
		staffName.setReadOnly(true);
		staffName.setFieldLabel("姓名");
		
		telPhone.setReadOnly(true);
		telPhone.setFieldLabel("联系电话");
		email.setFieldLabel("Email");
		email.setReadOnly(true);
		
		warnLevelCombo.setFieldLabel("告警级别");
		warnLevelCombo.setDisplayField("name");
		warnLevelCombo.setStore(UiUtil.generateStore(new String[]{"A","B","C"},new String[]{"A","B","C"}));
		warnLevelCombo.setAllowBlank(false);	
		warnLevelCombo.setTriggerAction(TriggerAction.ALL);
		warnLevelCombo.setEditable(false);
		
		warnModelCombo.setFieldLabel("告警方式");
		warnModelCombo.setAllowBlank(false);
		warnModelCombo.setDisplayField("name");
		warnModelCombo.setStore(UiUtil.generateStore(new String[]{"短信","Email","语音","软墙板"},new String[]{"2","4","3","1"}));
		warnModelCombo.setTriggerAction(TriggerAction.ALL);
		warnModelCombo.setEditable(false);
		
		stsCombo.setFieldLabel("状态");
		stsCombo.setAllowBlank(false);
		stsCombo.setDisplayField("name");
		stsCombo.setStore(UiUtil.generateStore(new String[]{"在用","不在用"},new String[]{"A","B"}));
		stsCombo.setTriggerAction(TriggerAction.ALL);
		stsCombo.setEditable(false);
		
		staffNo.addKeyListener(new KeyListener(){
			@Override
			public void componentKeyDown(ComponentEvent event) {
				if(event.getKeyCode()==KeyCodes.KEY_ENTER){
					AsyncCallback getMsgCallBack=new AsyncCallback(){
						public void onFailure(Throwable caught) {
							MessageBox.alert("alert",caught.getMessage(),null);
						}
						public void onSuccess(Object result) {
							Map eccStaffMsgMap=(Map)result;
							staffName.setValue((String)eccStaffMsgMap.get("staffName"));
							staffId.setValue((String)eccStaffMsgMap.get("staffId"));
							telPhone.setValue((String)eccStaffMsgMap.get("connNbr"));
							email.setValue((String)eccStaffMsgMap.get("email"));
						}
					};
					Map<String,String> inputparamMap=new HashMap<String,String>();
					inputparamMap.put("staffNo", staffNo.getValue());
					jsonRpc.request(GWT.getHostPageBaseURL()+ "scriptWarnAction/getEccStaffManagerByStaffNo.nut", inputparamMap, getMsgCallBack);
				}
			}});
		final Button btnAdd=new Button("确定");
		btnAdd.addSelectionListener(new SelectionListener<ButtonEvent>(){
			@Override
			public void componentSelected(ButtonEvent ce) {
				final ListStore<ModelData> listStore = (ListStore<ModelData>)Registry.get("PERSON_WARN_STORE");
				final ModelData currModelData=listStore.findModel("staffId", staffId.getValue());
				ModelData planModelData=planGrid.getSelectionModel().getSelectedItem();
				if(planModelData==null){
					MessageBox.alert("提示","请先选择计划",null);
					return ;
				}
				if("insert".equals(actionType.getValue())){
					if(currModelData!=null){
						MessageBox.alert("提示","已经存在<"+staffNo.getValue()+"的告警联系人",null);
						return ;
					}else {
						final ModelData baseModelData=new BaseModelData();
						baseModelData.set("staffName", staffName.getValue());
						baseModelData.set("staffNo", staffNo.getValue());
						baseModelData.set("warnLevel", warnLevelCombo.getValue().get("value"));
						baseModelData.set("connNbr", telPhone.getValue());
						baseModelData.set("email", email.getValue());
						baseModelData.set("warnMode", warnModelCombo.getValue().get("value"));
						baseModelData.set("staffId", staffId.getValue());
						baseModelData.set("sts", stsCombo.getValue().get("value"));
						baseModelData.set("planId", planModelData.get("planId"));
						AsyncCallback insertWarnStaffCallBack=new AsyncCallback(){
							public void onFailure(Throwable caught) {
								MessageBox.alert("alert",caught.getMessage(),null);
							}
							public void onSuccess(Object result) {
								if((Boolean)result){
									listStore.insert(baseModelData, 0);
									MessageBox.alert("提示","插入成功",null);
									formPanel.reset();
									hide();
								}
							}
						};
						jsonRpc.requestStream(GWT.getHostPageBaseURL()+ "scriptWarnAction/insertWarnStaff.nut", baseModelData.getProperties(), insertWarnStaffCallBack);
					}
				}else if("modify".equals(actionType.getValue())){
					if(currModelData==null){
						MessageBox.alert("提示","请先选择要修改的联系人",null);
						return ;
					}
					currModelData.set("staffName", staffName.getValue());
					currModelData.set("staffNo", staffNo.getValue());
					currModelData.set("warnLevel", warnLevelCombo.getValue().get("value"));
					currModelData.set("connNbr", telPhone.getValue());
					currModelData.set("email", email.getValue());
					currModelData.set("warnMode", warnModelCombo.getValue().get("value"));
					currModelData.set("staffId", staffId.getValue());
					currModelData.set("sts", stsCombo.getValue().get("value"));
					AsyncCallback updateWarnStaffCallBack=new AsyncCallback(){
						public void onFailure(Throwable caught) {
							MessageBox.alert("alert",caught.getMessage(),null);
						}
						public void onSuccess(Object result) {
							if((Boolean)result){
								listStore.update(currModelData);
								MessageBox.alert("提示","更新成功",null);
								formPanel.reset();
								hide();
							}
						}
					};
					jsonRpc.requestStream(GWT.getHostPageBaseURL()+ "scriptWarnAction/updateWarnStaff.nut", currModelData.getProperties(), updateWarnStaffCallBack);
				}
				
				
				
			}
			
		});
		formPanel.setHeaderVisible(true);
		formPanel.setButtonAlign(HorizontalAlignment.CENTER);
		formPanel.add(staffId);
		formPanel.add(staffNo);
		formPanel.add(staffName);
		formPanel.add(telPhone);
		formPanel.add(email);
		formPanel.add(warnLevelCombo);
		formPanel.add(warnModelCombo);
		formPanel.add(stsCombo);
		formPanel.addButton(btnAdd);
		formPanel.setHeaderVisible(false);
		return formPanel;
		
	}
	
	
	

}
