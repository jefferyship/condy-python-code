package ecc.warning.manager;

import java.text.SimpleDateFormat;
import java.util.Iterator;
import java.util.List;

import org.nutz.dao.Cnd;
import org.nutz.dao.Dao;

import ecc.warning.pojo.EccStaffManager;
import ecc.warning.pojo.WarnPlanInfo;
import ecc.warning.pojo.WarnScript;
import ecc.warning.pojo.WarnStaff;
import ecc.warning.util.NutDaoFactory;

public class ScriptWarnManager {
	public boolean insertScriptPlan(WarnPlanInfo warnPlanInfo){
		boolean bResult=false;
		Dao dao =NutDaoFactory.getNutDaoInstance();
		dao.insert(warnPlanInfo);
		bResult=true;
	return bResult;
	}
	
	public boolean updateScriptPlan(WarnPlanInfo warnPlanInfo){
		boolean bResult=false;
		Dao dao =NutDaoFactory.getNutDaoInstance();
		dao.updateIgnoreNull(warnPlanInfo);
		bResult=true;
	return bResult;
	}
	
	public boolean deleteScriptPlan(String planId){
		boolean bResult=false;
		Dao dao =NutDaoFactory.getNutDaoInstance();
		WarnPlanInfo warnPlanInfo=getScriptPlanById(planId);
		dao.fetchLinks(warnPlanInfo, "warnStaffList");
		if (warnPlanInfo!=null){
			dao.deleteWith(warnPlanInfo, "warnStaffList");
		}
		bResult=true;
	return bResult;
	}
	public List<WarnPlanInfo> listPlan(){
		SimpleDateFormat sdf=new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
		Dao dao =NutDaoFactory.getNutDaoInstance();
		List<WarnPlanInfo> list=dao.query(WarnPlanInfo.class, null, null);
		if(list!=null){
			for (WarnPlanInfo warnPlanInfo : list) {
				if(warnPlanInfo.getLastTime()!=null)
					warnPlanInfo.setLastTimeStr(sdf.format(warnPlanInfo.getLastTime()));
				if(warnPlanInfo.getNextTime()!=null)
					warnPlanInfo.setNextTimeStr(sdf.format(warnPlanInfo.getNextTime()));
			}
			
		}
		return list;
	}
	
	public WarnPlanInfo getScriptPlanById(String planId){
		Dao dao =NutDaoFactory.getNutDaoInstance();
		return dao.fetch(WarnPlanInfo.class, planId);
	}
	
	public boolean insertWarnStaff(WarnStaff warnStaff){
		boolean bResult=false;
		Dao dao =NutDaoFactory.getNutDaoInstance();
		dao.insert(warnStaff);
		bResult=true;
		return bResult;
	}
	
	public boolean deleteWarnStaff(WarnStaff warnStaff){
		boolean bResult=false;
		Dao dao =NutDaoFactory.getNutDaoInstance();
		dao.delete(warnStaff);
		bResult=true;
	return bResult;
	}
	public List<WarnStaff> listWarnStaff(String planId){
		Dao dao =NutDaoFactory.getNutDaoInstance();
		List<WarnStaff> list=dao.query(WarnStaff.class, Cnd.where("planId", "=", planId), null);
		if(list!=null){
			for (WarnStaff warnStaff : list) {
				dao.fetchLinks(warnStaff, "eccStaffManger"); 
				EccStaffManager eccStaffManager=warnStaff.getEccStaffManger();
				warnStaff.setStaffName(eccStaffManager.getStaffName());
				warnStaff.setStaffNo(eccStaffManager.getStaffNo());
				warnStaff.setConnNbr(eccStaffManager.getConnNbr());
				warnStaff.setEmail(eccStaffManager.getEmail());
				warnStaff.setEccStaffManger(null);
			}
		}
		return list;
	}
	
	
	public boolean insertWarnScript(WarnScript warnScript){
		boolean bResult=false;
		Dao dao =NutDaoFactory.getNutDaoInstance();
		dao.insert(warnScript);
		bResult=true;
	return bResult;
		
	}
	public boolean updateWarnScript(WarnScript warnScript){
		boolean bResult=false;
		Dao dao =NutDaoFactory.getNutDaoInstance();
		dao.update(warnScript);
		bResult=true;
	return bResult;
	}
	
	public boolean updateWarnStaff(WarnStaff warnStaff){
		boolean bResult=false;
		Dao dao =NutDaoFactory.getNutDaoInstance();
		dao.update(warnStaff);
		bResult=true;
	return bResult;
	}
	
	public boolean deleteWarnScript(String scriptId){
		boolean bResult=false;
		Dao dao =NutDaoFactory.getNutDaoInstance();
		dao.delete(WarnScript.class, scriptId);
		bResult=true;
	return bResult;
	}
	public WarnScript getWarnScriptById(String scriptId){
		Dao dao =NutDaoFactory.getNutDaoInstance();
		return dao.fetch(WarnScript.class, scriptId);
		
	}
	
	public List<WarnScript> listWarnScript(){
		Dao dao =NutDaoFactory.getNutDaoInstance();
		List<WarnScript> list=dao.query(WarnScript.class, null, null);
		return list;
	}
	
	public EccStaffManager getEccStaffManagerByStaffNo(String staffNo){
		Dao dao =NutDaoFactory.getNutDaoInstance();
		List<EccStaffManager> esmList=dao.query(EccStaffManager.class, Cnd.where("staffNo", "=", staffNo).and("sts", "=", "A"), null);
		if(esmList!=null && esmList.size()>0)
			return esmList.get(0);
		else
			return null;
		
	}
	
	
}	
	
	
	
	
	
