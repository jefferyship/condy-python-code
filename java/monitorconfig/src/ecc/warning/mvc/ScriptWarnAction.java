package ecc.warning.mvc;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.nutz.mvc.annotation.At;
import org.nutz.mvc.annotation.Ok;

import ecc.warning.manager.ScriptWarnManager;
import ecc.warning.pojo.WarnPlanInfo;
import ecc.warning.pojo.WarnScript;
import ecc.warning.pojo.WarnStaff;

public class ScriptWarnAction {
	ScriptWarnManager swm=new ScriptWarnManager();
	@At("scriptWarnAction/warnPlanList")
	@Ok("json")
	public Map warnPlanList(){
		List<WarnPlanInfo> list=swm.listPlan();
		Map<String,List> jsonMap=new HashMap<String,List>();
		jsonMap.put("records", list);
		return jsonMap;
	}
	@At("scriptWarnAction/warnStaffList")
	@Ok("json")
	public Map warnStaffList(String planId){
		List<WarnStaff> list=swm.listWarnStaff(planId);
		Map<String,List> jsonMap=new HashMap<String,List>();
		jsonMap.put("records", list);
		return jsonMap;
	}
	@At("scriptWarnAction/getWarnScript")
	@Ok("json")
	public WarnScript getWarnScript(String scriptId){
		WarnScript warnScript=swm.getWarnScriptById(scriptId);
		return warnScript;
	}
	

}
