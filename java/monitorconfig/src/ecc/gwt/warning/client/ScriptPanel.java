package ecc.gwt.warning.client;

import java.util.logging.Logger;

import com.extjs.gxt.ui.client.Registry;
import com.extjs.gxt.ui.client.Style.LayoutRegion;
import com.extjs.gxt.ui.client.data.BaseListLoader;
import com.extjs.gxt.ui.client.data.HttpProxy;
import com.extjs.gxt.ui.client.data.JsonLoadResultReader;
import com.extjs.gxt.ui.client.data.ListLoadResult;
import com.extjs.gxt.ui.client.data.ModelData;
import com.extjs.gxt.ui.client.data.ModelType;
import com.extjs.gxt.ui.client.store.ListStore;
import com.extjs.gxt.ui.client.widget.ContentPanel;
import com.extjs.gxt.ui.client.widget.LayoutContainer;
import com.extjs.gxt.ui.client.widget.form.ListField;
import com.extjs.gxt.ui.client.widget.layout.BorderLayout;
import com.extjs.gxt.ui.client.widget.layout.BorderLayoutData;
import com.extjs.gxt.ui.client.widget.layout.FitLayout;
import com.google.gwt.core.client.GWT;
import com.google.gwt.http.client.RequestBuilder;
/**
 * 脚本的配置窗口
 * @author 林桦
 *
 */
public class ScriptPanel extends LayoutContainer {

	private Logger logger;
	private ListStore<ModelData> listStore;
	public ScriptPanel() {
		logger=Logger.getLogger("ecc.gwt.warning.client");
		generatePlanStore();
		setLayout(new BorderLayout());
		BorderLayoutData westLayoutData=new BorderLayoutData(LayoutRegion.EAST,28);
		BorderLayoutData centerLayoutData=new BorderLayoutData(LayoutRegion.CENTER);
		add(createNavPanel(),westLayoutData);
	}
	/**
	 *生成PlanStore。存储在PLAN_STORE关键字.
	 */
	private void generatePlanStore(){
		RequestBuilder builder=new RequestBuilder(RequestBuilder.GET,GWT.getHostPageBaseURL()+"data/rssReader.json");
		HttpProxy<String> httpProxy=new HttpProxy<String>(builder);
		ModelType rssReaderModelType=new ModelType();
		rssReaderModelType.setRoot("records");
		rssReaderModelType.addField("description");
		rssReaderModelType.addField("link");
		rssReaderModelType.addField("title");
		rssReaderModelType.addField("uuid");
		JsonLoadResultReader<ListLoadResult<ModelData>> reader=new JsonLoadResultReader<ListLoadResult<ModelData>>(rssReaderModelType);
		final BaseListLoader<ListLoadResult<ModelData>> loader=new BaseListLoader<ListLoadResult<ModelData>>(httpProxy,reader);
		listStore=new ListStore<ModelData>(loader);
	}
	/**
	 * 生成PlanPanel.
	 * @return
	 */
	private ContentPanel createNavPanel(){
		ContentPanel navPanel=new ContentPanel();
		ListField<ModelData> feeList=new ListField<ModelData>();
		feeList.setStore(listStore);
		feeList.setDisplayField("plan_name");
		navPanel.add(feeList);
		navPanel.setLayout(new FitLayout());
		return navPanel;
	}

}
