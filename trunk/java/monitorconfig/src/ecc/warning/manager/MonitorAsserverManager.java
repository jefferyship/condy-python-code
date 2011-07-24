package ecc.warning.manager;

import java.util.ArrayList;
import java.util.List;

import org.nutz.dao.Cnd;
import org.nutz.dao.Dao;

import ecc.warning.pojo.MonitorAsserver;
import ecc.warning.util.NutDaoFactory;

public class MonitorAsserverManager {
	
	public boolean  insert(MonitorAsserver ma){
		boolean bResult=false;
			Dao dao =NutDaoFactory.getNutDaoInstance();
			dao.insert(ma);
			bResult=true;
		return bResult;

	}
	
	public boolean update(MonitorAsserver ma){
		boolean bResult=false;
		Dao dao =NutDaoFactory.getNutDaoInstance();
		dao.update(ma);
		bResult=true;
	
	return bResult;
	}
	
	public boolean delete(String seq){
		boolean bResult=false;
		Dao dao =NutDaoFactory.getNutDaoInstance();
		dao.delete(MonitorAsserver.class, seq);
		bResult=true;
	
	return bResult;
	}
	
	public List<MonitorAsserver> list(String searchType,String searchContent){
		Dao dao =NutDaoFactory.getNutDaoInstance();
		List<MonitorAsserver> list;
		if(searchType==null||"null".equals("searchType")||searchContent==null||"null".equals(searchContent))
			list= dao.query(MonitorAsserver.class, null, null);
		else
			list=dao.query(MonitorAsserver.class, Cnd.where(searchType, "like", "%"+searchContent+"%"), null);
		return list;
		
	}
	
	
	
	public MonitorAsserver getBySeq(String seq){
		Dao dao =NutDaoFactory.getNutDaoInstance();
		return dao.fetch(MonitorAsserver.class, seq);
	}
	

}
