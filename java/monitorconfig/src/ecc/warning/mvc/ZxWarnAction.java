package ecc.warning.mvc;


import java.sql.Timestamp;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.nutz.json.Json;
import org.nutz.mvc.adaptor.PairAdaptor;
import org.nutz.mvc.annotation.AdaptBy;
import org.nutz.mvc.annotation.At;
import org.nutz.mvc.annotation.Ok;
import org.nutz.mvc.annotation.Param;

import ecc.warning.manager.ZxWarnManager;
import ecc.warning.pojo.ZxAlarmConfig;
import ecc.warning.pojo.ZxAlarmLog;

public class ZxWarnAction {
	ZxWarnManager mam=new ZxWarnManager();
	@At("zxWarn/getAlarmLog")
	@AdaptBy(type=PairAdaptor.class)
	@Ok("json")
	public Map getAlarmLog(@Param("startDate")String startDate,@Param("endDate")String endDate
			,@Param("alarmLevel")String alarmLevel
			,@Param("alarmTypeId")String alarmTypeId
			,@Param("offset")String offset
			,@Param("limit")String limit
			,@Param("totalCount")String totalCount){
		System.out.println("startDate:"+startDate);
		System.out.println("alarmLevel:"+alarmLevel);
		System.out.println("alarmTypeId:"+alarmTypeId);
		System.out.println("offset:"+offset);
		System.out.println("limit:"+limit);
		System.out.println("totalCount:"+totalCount);
		/*List<ZxAlarmLog> list=new ArrayList<ZxAlarmLog>();
		for (int i = 0; i < 10; i++) {
			ZxAlarmLog zxAlarmLog=new ZxAlarmLog();
			zxAlarmLog.setAlarmLevel("1");
			zxAlarmLog.setAlarmSeq(""+i);
			zxAlarmLog.setAlarmTime(new Timestamp(System.currentTimeMillis()));
			zxAlarmLog.setAlarmTypeId("pcm");
			zxAlarmLog.setLogType("1");
			zxAlarmLog.setRecoverTime(new Timestamp(System.currentTimeMillis()));
			zxAlarmLog.setRemark("aabbb");
			list.add(zxAlarmLog);
		}*/
		
		int realTotalCount=0;
		if(totalCount==null||"".equals(totalCount))
			realTotalCount=mam.getZxAlarmLogOfCount(startDate, endDate, alarmLevel, alarmTypeId);
		else
			realTotalCount=Integer.parseInt(totalCount);
		List<ZxAlarmLog> list=mam.getZxAlarmLog(startDate, endDate, alarmLevel, alarmTypeId, Integer.parseInt(offset), Integer.parseInt(limit),realTotalCount);
		Map jsonMap=new HashMap();
		jsonMap.put("records", list);
		jsonMap.put("total", realTotalCount);
		return jsonMap;
		//return Json.toJson(ma.getSeq());
	}
	@At("zxWarn/getAlarmConfig")
	@Ok("json")
	public Map getAlarmConfig(){
		List<ZxAlarmConfig> list=new ArrayList<ZxAlarmConfig>();
		list=mam.getAlarmConfig();
		ZxAlarmConfig zxAlarmConfig=new ZxAlarmConfig();
		zxAlarmConfig.setAlarmTypeId("all");
		zxAlarmConfig.setAlarmName("Ыљга");
		list.add(0, zxAlarmConfig);
		Map jsonMap=new HashMap();
		jsonMap.put("records", list);
		System.out.println(Json.toJson(jsonMap));
		return jsonMap;
	}
	
}
