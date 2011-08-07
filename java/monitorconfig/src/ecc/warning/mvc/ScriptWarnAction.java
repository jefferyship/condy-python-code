package ecc.warning.mvc;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.nutz.mvc.adaptor.JsonAdaptor;
import org.nutz.mvc.annotation.AdaptBy;
import org.nutz.mvc.annotation.At;
import org.nutz.mvc.annotation.Ok;
import org.nutz.mvc.annotation.Param;

import ecc.warning.manager.ScriptWarnManager;
import ecc.warning.pojo.EccStaffManager;
import ecc.warning.pojo.JsonReturnObjectOfGwt;
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
	public JsonReturnObjectOfGwt getWarnScript(String scriptId){
		WarnScript warnScript=swm.getWarnScriptById(scriptId);
		JsonReturnObjectOfGwt result=new JsonReturnObjectOfGwt();
		if(warnScript==null)
			result.setResult(new WarnScript());
		else
			result.setResult(warnScript);
		return result;
	}
	@At("scriptWarnAction/insertWarnScript")
	@AdaptBy(type=JsonAdaptor.class)
	@Ok("json")
	public JsonReturnObjectOfGwt insertWarnScript(WarnScript warnScript){
		boolean bResult=swm.insertWarnScript(warnScript);
		JsonReturnObjectOfGwt result=new JsonReturnObjectOfGwt();
		result.setResult(warnScript.getScriptId());
		return result;
	}
	
	@At("scriptWarnAction/updateWarnScript")
	@AdaptBy(type=JsonAdaptor.class)
	@Ok("json")
	public JsonReturnObjectOfGwt updateWarnScript(WarnScript warnScript){
		boolean bResult=swm.updateWarnScript(warnScript);
		JsonReturnObjectOfGwt result=new JsonReturnObjectOfGwt();
		result.setResult(bResult);
		return result;
	}
	@At("scriptWarnAction/planConfirmWarnScript")
	@AdaptBy(type=JsonAdaptor.class)
	@Ok("json")
	public JsonReturnObjectOfGwt planConfirmWarnScript(@Param("planId")String planId,@Param("scriptId")String scriptId){
		WarnPlanInfo warnPlanInfo=new WarnPlanInfo();
		warnPlanInfo.setPlanId(planId);
		warnPlanInfo.setScriptId(scriptId);
		boolean bResult=swm.updateScriptPlan(warnPlanInfo);
		JsonReturnObjectOfGwt result=new JsonReturnObjectOfGwt();
		result.setResult(bResult);
		return result;
	}
	@At("scriptWarnAction/listWarnScript")
	@Ok("json")
	public Map listWarnScript(){
		List<WarnScript> list=swm.listWarnScript();
		Map<String,List> jsonMap=new HashMap<String,List>();
		jsonMap.put("records", list);
		return jsonMap;
	}
	@At("scriptWarnAction/getEccStaffManagerByStaffNo")
	@Ok("json")
	public JsonReturnObjectOfGwt getEccStaffManagerByStaffNo(@Param("staffNo")String staffNo){
		EccStaffManager esm=swm.getEccStaffManagerByStaffNo(staffNo);
		JsonReturnObjectOfGwt result=new JsonReturnObjectOfGwt();
		if(esm==null)
			result.setError("无法取到<"+staffNo+">的员工信息");
		else
			result.setResult(esm);
		return result;
	}
	@At("scriptWarnAction/deleteScriptPlan")
	@Ok("json")
	public JsonReturnObjectOfGwt deleteScriptPlan(@Param("planId")String planId){
		boolean bResult=swm.deleteScriptPlan(planId);
		JsonReturnObjectOfGwt result=new JsonReturnObjectOfGwt();
		result.setResult(bResult);
		return result;
	}
	@At("scriptWarnAction/insertScriptPlan")
	@Ok("json")
	public JsonReturnObjectOfGwt insertScriptPlan(WarnPlanInfo warnPlanInfo){
		boolean bResult=swm.insertScriptPlan(warnPlanInfo);
		JsonReturnObjectOfGwt result=new JsonReturnObjectOfGwt();
		result.setResult(bResult);
		return result;
	}
	
	@At("scriptWarnAction/updateScriptPlan")
	@Ok("json")
	public JsonReturnObjectOfGwt updateScriptPlan(WarnPlanInfo warnPlanInfo){
		boolean bResult=swm.updateScriptPlan(warnPlanInfo);
		JsonReturnObjectOfGwt result=new JsonReturnObjectOfGwt();
		result.setResult(bResult);
		return result;
	}
	
	

}
