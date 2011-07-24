package ecc.gwt.warning.client;

import com.extjs.gxt.ui.client.data.BaseModelData;
import com.extjs.gxt.ui.client.data.ModelData;
import com.extjs.gxt.ui.client.store.ListStore;

public class UiUtil {
	/**
	 * 生成combo的store对象，paramList 大小必须和valueList大小保持一致.
	 * @param String[] names 名称列
	 * @param valueLis 值列
	 * @return
	 */
	public static ListStore<ModelData> generateStore(String[] names,String[] values){
		ListStore<ModelData> listStore=new ListStore<ModelData>();
		for (int i = 0; i < names.length; i++) {
			ModelData modelData=new BaseModelData();
			modelData.set("name", names[i]);
			modelData.set("value", values[i]);
			listStore.add(modelData);
		}
	    return listStore;
	}

}
