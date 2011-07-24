package ecc.warning.mvc;


import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.nutz.json.Json;
import org.nutz.mvc.adaptor.JsonAdaptor;
import org.nutz.mvc.adaptor.PairAdaptor;
import org.nutz.mvc.annotation.AdaptBy;
import org.nutz.mvc.annotation.At;
import org.nutz.mvc.annotation.Ok;
import org.nutz.mvc.annotation.Param;

import ecc.warning.manager.MonitorAsserverManager;
import ecc.warning.pojo.JsonReturnObjectOfGwt;
import ecc.warning.pojo.MonitorAsserver;

public class MonitorAsserverAction {
	MonitorAsserverManager mam=new MonitorAsserverManager();
	@At("monitorAsserver/insert")
	@AdaptBy(type=JsonAdaptor.class)
	@Ok("json")
	public JsonReturnObjectOfGwt insert(MonitorAsserver ma){
		System.out.println("getMonitorName:"+ma.getMonitorName());
		boolean bResult=mam.insert(ma);
		JsonReturnObjectOfGwt result=new JsonReturnObjectOfGwt();
		result.setResult(ma.getSeq());
		return result;
		//return Json.toJson(ma.getSeq());
	}
	@At("monitorAsserver/list")
	@Ok("json")
	public Map list(@Param("searchType")String searchType,@Param("searchContent")String searchContent){
		List<MonitorAsserver> list=null;
		list=mam.list(searchType, searchContent);
		Map<String,List> jsonMap=new HashMap<String,List>();
		jsonMap.put("records", list);
		//System.out.println(Json.toJson(jsonMap));
		return jsonMap;
		//return  Json.toJson(jsonMap);
	}
	
	@At("monitorAsserver/update")
	@AdaptBy(type=JsonAdaptor.class)
	@Ok("json")
	public JsonReturnObjectOfGwt update(MonitorAsserver ma){
		System.out.println("getMonitorName:"+ma.getMonitorName());
		boolean bResult=mam.update(ma);
		JsonReturnObjectOfGwt result=new JsonReturnObjectOfGwt();
		result.setResult(bResult);
		return result;
	}
	
	@At("monitorAsserver/delete")
	@Ok("json")
	public JsonReturnObjectOfGwt delete(@Param("seq")String seq){
		System.out.println("seq:"+seq);
		boolean bResult=mam.delete(seq);
		JsonReturnObjectOfGwt result=new JsonReturnObjectOfGwt();
		result.setResult(bResult);
		return result;
	}

}
