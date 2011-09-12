package ecc.warning.mvc;


import java.sql.Timestamp;
import java.util.ArrayList;
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
import ecc.warning.pojo.ZxAlarmConfig;
import ecc.warning.pojo.ZxAlarmLog;

public class ZxWarnAction {
	MonitorAsserverManager mam=new MonitorAsserverManager();
	@At("zxWarn/getAlarmLog")
	@AdaptBy(type=PairAdaptor.class)
	@Ok("json")
	public Map getAlarmLog(@Param("startDate")String startDate,@Param("endDate")String endDate
			,@Param("alarmLevel")String alarmLevel
			,@Param("alarmTypeId")String alarmTypeId
			,@Param("offset")String offset
			,@Param("limit")String limit){
		System.out.println("startDate:"+startDate);
		System.out.println("alarmLevel:"+alarmLevel);
		System.out.println("alarmTypeId:"+alarmTypeId);
		System.out.println("offset:"+offset);
		List<ZxAlarmLog> list=new ArrayList<ZxAlarmLog>();
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
		}
		Map jsonMap=new HashMap();
		jsonMap.put("records", list);
		jsonMap.put("total", 60);
		System.out.println(Json.toJson(jsonMap));
		return jsonMap;
		//return Json.toJson(ma.getSeq());
	}
	@At("zxWarn/getAlarmConfig")
	@Ok("json")
	public Map getAlarmConfig(){
		List<ZxAlarmConfig> list=new ArrayList<ZxAlarmConfig>();
		ZxAlarmConfig zxAlarmConfig=new ZxAlarmConfig();
		zxAlarmConfig.setAlarmLevel("1");
		zxAlarmConfig.setAlarmName("PCM¸æ¾¯");
		zxAlarmConfig.setAlarmTypeId("pcm");
		list.add(zxAlarmConfig);
		Map jsonMap=new HashMap();
		jsonMap.put("records", list);
		System.out.println(Json.toJson(jsonMap));
		return jsonMap;
	}
	
}
