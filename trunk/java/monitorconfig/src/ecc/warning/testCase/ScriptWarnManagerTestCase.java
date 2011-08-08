package ecc.warning.testCase;

import java.util.List;

import org.nutz.json.Json;

import ecc.warning.manager.ScriptWarnManager;
import ecc.warning.pojo.WarnPlanInfo;
import ecc.warning.pojo.WarnScript;
import ecc.warning.pojo.WarnStaff;
import junit.framework.TestCase;

public class ScriptWarnManagerTestCase extends TestCase {

	private ScriptWarnManager scriptWarnManager;
	protected void setUp() throws Exception {
		super.setUp();
		scriptWarnManager=new ScriptWarnManager();
	}
	public void testListPlan(){
		List<WarnPlanInfo> list=scriptWarnManager.listPlan();
		assertNotNull(list);
		assertFalse(list.size()==0);
		System.out.println(list.get(0).getPlanName());
	}
	public void testInsertPlan(){
		WarnPlanInfo warnPlanInfo=new WarnPlanInfo();
		warnPlanInfo.setAreaCode("0591");
		warnPlanInfo.setCompanyId("1");
		warnPlanInfo.setBeginHours("10");
		warnPlanInfo.setDataTagId("0591");
		warnPlanInfo.setEndHours("15");
		warnPlanInfo.setPlanName("œµÕ≥≤‚ ‘");
		warnPlanInfo.setRemark("aaaaaaaaaaa");
		boolean bResult=scriptWarnManager.insertScriptPlan(warnPlanInfo);
		assertTrue(bResult);
		assertNotNull(warnPlanInfo.getPlanId());
	}
	
	public void testUpatePlan(){
		WarnPlanInfo warnPlanInfo=scriptWarnManager.getScriptPlanById("4");
		warnPlanInfo.setRemark("cccccccc");
		assertTrue(scriptWarnManager.updateScriptPlan(warnPlanInfo));
	}
	
	public void deletePlan(){
		assertTrue(scriptWarnManager.deleteScriptPlan("4"));
		
	}
	public void testlistWarnStaff(){
		List<WarnStaff> list=scriptWarnManager.listWarnStaff("3");
		assertNotNull(list);
		assertFalse(list.size()==0);
		
		System.out.println(Json.toJson(list));
	}
	
	public void testInsertWarnScript(){
		WarnScript warnScript=new WarnScript();
		warnScript.setScriptRemark("ccc");
		warnScript.setScriptbash("aaaaaaaaaaaa");
		warnScript.setSts("A");
		assertTrue(scriptWarnManager.insertWarnScript(warnScript));
		
		
	}

}
