package ecc.gwt.warning.client;

import com.extjs.gxt.ui.client.data.BaseModelData;
import com.extjs.gxt.ui.client.data.ModelData;
import com.extjs.gxt.ui.client.store.ListStore;

public class UiUtil {
	/**
	 * ����combo��store����paramList ��С�����valueList��С����һ��.
	 * @param String[] names ������
	 * @param valueLis ֵ��
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
