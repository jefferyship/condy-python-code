package ecc.gwt.warning.client;

import java.util.logging.Logger;

import com.extjs.gxt.ui.client.Style.LayoutRegion;
import com.extjs.gxt.ui.client.event.ButtonEvent;
import com.extjs.gxt.ui.client.event.SelectionListener;
import com.extjs.gxt.ui.client.widget.ContentPanel;
import com.extjs.gxt.ui.client.widget.TabItem;
import com.extjs.gxt.ui.client.widget.TabPanel;
import com.extjs.gxt.ui.client.widget.Viewport;
import com.extjs.gxt.ui.client.widget.button.Button;
import com.extjs.gxt.ui.client.widget.layout.BorderLayout;
import com.extjs.gxt.ui.client.widget.layout.BorderLayoutData;
import com.extjs.gxt.ui.client.widget.layout.FitLayout;
import com.extjs.gxt.ui.client.widget.toolbar.SeparatorToolItem;
import com.extjs.gxt.ui.client.widget.toolbar.ToolBar;
import com.google.gwt.core.client.EntryPoint;
import com.google.gwt.user.client.ui.RootPanel;

/**
 * Entry point classes define <code>onModuleLoad()</code>.
 */
public class ImageViewer implements EntryPoint {
	private TabPanel tabPanel=new TabPanel();
	private Logger logger;
	public void onModuleLoad() {
		logger=Logger.getLogger("ecc.gwt.warning.client");
		RootPanel rootPanel = RootPanel.get();
		Viewport viewPort=new Viewport();
		viewPort.setLayout(new BorderLayout());
		BorderLayoutData northLayoutData=new BorderLayoutData(LayoutRegion.NORTH,28);
		BorderLayoutData centerLayoutData=new BorderLayoutData(LayoutRegion.CENTER);
		viewPort.add(getRootContentPanel(),northLayoutData);
		viewPort.add(getTabPanel(),centerLayoutData);
		
		rootPanel.add(viewPort);
		
	}
	private ContentPanel getRootContentPanel(){
		ContentPanel rootContentPanel=new ContentPanel();
		rootContentPanel.setHeaderVisible(false);
		rootContentPanel.setLayout(new FitLayout());
		ToolBar toolbar=new ToolBar();
		Button scriptWarnButton=new Button("脚本告警配置");
		scriptWarnButton.setItemId("script");
		Button ptWarnButton=new Button("平台告警配置");
		ptWarnButton.setItemId("pt");
		Button zxWarnButton=new Button("中兴告警配置");
		zxWarnButton.setItemId("zx");
		Button webServerWarnButton=new Button("应用服务器告警配置");
		webServerWarnButton.setItemId("webserver");
		final SelectionListener<ButtonEvent> tabButtonSelectionListener=new SelectionListener<ButtonEvent>(){
			@Override
			public void componentSelected(ButtonEvent ce) {
				Button button=ce.getButton();
				String itemId=button.getItemId();
				TabItem tabItem=tabPanel.getItemByItemId("tab"+itemId);
				if(tabItem==null){
					tabItem=new TabItem();
					tabItem.setText(button.getText());
					tabItem.setId("tab"+itemId);
					tabItem.setClosable(true);
					if ("webserver".equals(itemId)){
						tabItem.add(new WebServerConfigGrid());
					}else if("script".equals(itemId)){
						tabItem.add(new ScriptWarnConfigPanel());
					}else if("zx".equals(itemId)){
						tabItem.add(new ZXWarnViewPanel());
					}
					tabPanel.add(tabItem);
					tabPanel.setSelection(tabItem);
						
				}else{
					tabPanel.setSelection(tabItem);
				}
			}
		};
		scriptWarnButton.addSelectionListener(tabButtonSelectionListener);
		ptWarnButton.addSelectionListener(tabButtonSelectionListener);
		zxWarnButton.addSelectionListener(tabButtonSelectionListener);
		webServerWarnButton.addSelectionListener(tabButtonSelectionListener);
		toolbar.add(scriptWarnButton);
		toolbar.add(new SeparatorToolItem());
		toolbar.add(ptWarnButton);
		toolbar.add(new SeparatorToolItem());
		toolbar.add(zxWarnButton);
		toolbar.add(new SeparatorToolItem());
		toolbar.add(webServerWarnButton);
		rootContentPanel.setTopComponent(toolbar);
		return rootContentPanel;
	}
	private TabPanel getTabPanel(){
		/*TabItem tabItem=new TabItem();
		tabItem.setText("aaaa");
		tabItem.setClosable(true);
		tabPanel.add(tabItem);*/
		
		return tabPanel;
	}
}