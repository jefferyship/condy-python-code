package ecc.warning.manager;

import java.util.List;

import org.nutz.dao.Cnd;
import org.nutz.dao.Condition;
import org.nutz.dao.Dao;
import org.nutz.dao.DatabaseMeta;
import org.nutz.dao.pager.OraclePager;
import org.nutz.dao.pager.Pager;

import ecc.warning.pojo.ZxAlarmConfig;
import ecc.warning.pojo.ZxAlarmDetailLog;
import ecc.warning.pojo.ZxAlarmLog;
import ecc.warning.util.NutDaoFactory;

public class ZxWarnManager {
	public List<ZxAlarmConfig> getAlarmConfig(){
		Dao dao =NutDaoFactory.getNutDaoInstance();
		List<ZxAlarmConfig> list=dao.query(ZxAlarmConfig.class, null, null);
		return list;
	}
	
	public List<ZxAlarmLog> getZxAlarmLog(String startDate,String endDate,String alarmLevel,
			String alarmTypeId,int offset,int limit,int totalCount){
		//SimpleDateFormat sdf=new SimpleDateFormat("yyyy-MM-dd");
		Dao dao =NutDaoFactory.getNutDaoInstance();
		StringBuffer sbCondition=new StringBuffer();
		sbCondition.append("1=1  ");
		if (startDate!=null && !"".equals(startDate)){
			sbCondition.append("and alarm_Time>=to_date('").append(startDate).append("','yyyy-mm-dd') ");
		}
		if (endDate!=null && !"".equals(endDate)){
			sbCondition.append("and alarm_Time<=to_date('").append(endDate).append("','yyyy-mm-dd') ");
		}
		
		if(alarmLevel!=null&&!alarmLevel.equals("")&&!alarmLevel.equals("all"))
			sbCondition.append("and alarm_Level='").append(alarmLevel).append("' ");
		
		if(alarmTypeId!=null&&!alarmTypeId.equals("")&&!alarmTypeId.equals("all"))
			sbCondition.append("and alarm_Type_Id='").append(alarmTypeId).append("' ");
	
		/*Cnd cnd=Cnd.where("alarmTime",">=",startDate);
		if (endDate!=null){
			cnd=cnd.and("alarmTime","<=",endDate);
		}
		if(alarmLevel!=null&&!alarmLevel.equals(""))
			cnd=cnd.and("alarmLevel","=",alarmLevel);
		if(alarmTypeId!=null&&!alarmTypeId.equals(""))
			cnd=cnd.and("alarmTypeId","=",alarmTypeId);*/
		Condition cnd=Cnd.wrap(sbCondition.toString());
		//Pager pager=dao.createPager(offset, limit);
		//System.out.println("ccccccccccc:"+dao.createPager(10, 20));
		Pager pager=new OraclePager();
		pager.setPageNumber(2);
		pager.setPageSize(10);
		pager.setRecordCount(totalCount);
		int pageNumber=1;
		if(offset>0)
			pageNumber=offset/limit;
		List<ZxAlarmLog> list=dao.query(ZxAlarmLog.class, cnd, dao.createPager(pageNumber, limit));
		
		if(list!=null){
			for (ZxAlarmLog zxAlarmLog : list) {
				dao.fetchLinks(zxAlarmLog, "zxAlaramDetailLogList");
				List<ZxAlarmDetailLog> zxAlaramDetailLogList=zxAlarmLog.getZxAlaramDetailLogList();
				if (zxAlaramDetailLogList!=null){
					StringBuffer sbDetail=new StringBuffer();
					for (ZxAlarmDetailLog zxAlarmDetailLog : zxAlaramDetailLogList) {
						sbDetail.append(zxAlarmDetailLog.getAlarmItemId()).append("=").append(zxAlarmDetailLog.getAlarmItemValue()).append(" ");
					}
					zxAlarmLog.setRemark(sbDetail.toString());
					zxAlarmLog.setZxAlaramDetailLogList(null);
				}
			}
		}
		return list;
	}
	
	public int getZxAlarmLogOfCount(String startDate,String endDate,String alarmLevel,
			String alarmTypeId){
		Dao dao =NutDaoFactory.getNutDaoInstance();
		StringBuffer sbCondition=new StringBuffer();
		sbCondition.append("1=1  ");
		if (startDate!=null && !"".equals(startDate)){
			sbCondition.append("and alarm_Time>=to_date('").append(startDate).append("','yyyy-mm-dd') ");
		}
		if (endDate!=null && !"".equals(endDate)){
			sbCondition.append("and alarm_Time<=to_date('").append(endDate).append("','yyyy-mm-dd') ");
		}
		
		if(alarmLevel!=null&&!alarmLevel.equals("")&&!alarmLevel.equals("all"))
			sbCondition.append("and alarm_Level='").append(alarmLevel).append("' ");
		
		if(alarmTypeId!=null&&!alarmTypeId.equals("")&&!alarmTypeId.equals("all"))
			sbCondition.append("and alarm_Type_Id='").append(alarmTypeId).append("' ");
		Condition cnd=Cnd.wrap(sbCondition.toString());
		int totalCount=dao.count(ZxAlarmLog.class, cnd);
		return totalCount;
	}
	
}	
	
	
	
	
	
