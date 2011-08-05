package ecc.gwt.warning.client;


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
import com.extjs.gxt.ui.client.widget.Window;
import com.extjs.gxt.ui.client.widget.button.Button;
import com.extjs.gxt.ui.client.widget.form.ComboBox;
import com.extjs.gxt.ui.client.widget.form.FormPanel;
import com.extjs.gxt.ui.client.widget.form.HiddenField;
import com.extjs.gxt.ui.client.widget.form.TextField;
import com.extjs.gxt.ui.client.widget.form.ComboBox.TriggerAction;
import com.extjs.gxt.ui.client.widget.grid.Grid;
import com.extjs.gxt.ui.client.widget.layout.FitLayout;
import com.google.gwt.event.dom.client.KeyCodes;
import com.google.gwt.user.client.Element;

public class ScriptWarningPersonPopup extends Window {
	private final HiddenField<String> staffId=new HiddenField<String>();
	private final TextField<String> staffNo=new TextField<String>();
	private final TextField<String> staffName=new TextField<String>();
	private final TextField<String> telPhone=new TextField<String>();
	private final ComboBox<ModelData> warnLevelCombo = new ComboBox<ModelData>();
	private final ComboBox<ModelData> warnModelCombo = new ComboBox<ModelData>();
	private final Grid<ModelData> planGrid;
	private Logger logger;
	private final FormPanel formPanel=new FormPanel();
	public ScriptWarningPersonPopup(Grid<ModelData> planGrid){
		logger=Logger.getLogger("ecc.gwt.warning.client.ScriptWarnConfigPanel");
		this.planGrid=planGrid;
		setSize(350, 250);
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
		
		warnLevelCombo.setFieldLabel("告警级别");
		warnLevelCombo.setDisplayField("name");
		warnLevelCombo.setStore(UiUtil.generateStore(new String[]{"A","B","C"},new String[]{"A","B","C"}));
		warnLevelCombo.setAllowBlank(false);	
		warnLevelCombo.setTriggerAction(TriggerAction.ALL);
		warnLevelCombo.setEditable(false);
		
		warnModelCombo.setFieldLabel("告警方式");
		warnModelCombo.setAllowBlank(false);
		warnModelCombo.setDisplayField("name");
		warnModelCombo.setStore(UiUtil.generateStore(new String[]{"短信"},new String[]{"2"}));
		warnModelCombo.setTriggerAction(TriggerAction.ALL);
		warnModelCombo.setEditable(false);
		
		staffNo.addKeyListener(new KeyListener(){
			@Override
			public void componentKeyDown(ComponentEvent event) {
				if(event.getKeyCode()==KeyCodes.KEY_ENTER){
					staffId.setValue("5910");
					staffName.setValue("林桦");
					telPhone.setValue("18959130026");
				}
			}});
		final Button btnAdd=new Button("确定");
		btnAdd.addSelectionListener(new SelectionListener<ButtonEvent>(){
			@Override
			public void componentSelected(ButtonEvent ce) {
				addToWarnPersonStore();
			}
			
		});
		formPanel.setHeaderVisible(true);
		formPanel.setButtonAlign(HorizontalAlignment.CENTER);
		formPanel.add(staffId);
		formPanel.add(staffNo);
		formPanel.add(staffName);
		formPanel.add(telPhone);
		formPanel.add(warnLevelCombo);
		formPanel.add(warnModelCombo);
		formPanel.addButton(btnAdd);
		formPanel.addButton(new Button("重置",new SelectionListener<ButtonEvent>(){
			public void componentSelected(ButtonEvent ce) {
				formPanel.reset();
			}
			
		}));
		return formPanel;
		
	}
	
	private void addToWarnPersonStore(){
		//@TODO 将告警联系人插入数据库.
		ListStore<ModelData> listStore = (ListStore<ModelData>)Registry.get("PERSON_WARN_STORE");
		ListStore<ModelData> storeList=listStore;
		ModelData baseModelData=new BaseModelData();
		baseModelData.set("staffName", staffName.getValue());
		baseModelData.set("staffNo", staffNo.getValue());
		baseModelData.set("warnLevel", warnLevelCombo.getValue());
		baseModelData.set("telPhone", telPhone.getValue());
		baseModelData.set("warnMode", warnModelCombo.getValue());
		storeList.insert(baseModelData, 0);
		formPanel.reset();
		this.hide();
	}
	
	

}
