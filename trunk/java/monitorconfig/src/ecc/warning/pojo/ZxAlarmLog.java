package ecc.warning.pojo;

import java.sql.Timestamp;
import java.util.List;

import org.nutz.dao.entity.annotation.Column;
import org.nutz.dao.entity.annotation.Many;
import org.nutz.dao.entity.annotation.Name;
import org.nutz.dao.entity.annotation.Table;

@Table("monitor_zx_alarm_log")
public class ZxAlarmLog {
	@Name
	@Column("alarm_seq")
	private String alarmSeq;
	@Column("alarm_time")
	private Timestamp alarmTime;
	@Column("alarm_type_id")
	private String alarmTypeId;
	@Column("alarm_level")
	private String alarmLevel;
	@Column("log_type")
	private String logType;
	@Column("host_name")
	private String hostName;
	@Column("recover_time")
	private Timestamp recoverTime;
	@Column("remark")
	private String remark;
	@Many(target=ZxAlarmDetailLog.class,field="alarmSeq")
	private List<ZxAlarmDetailLog> zxAlaramDetailLogList;
	
	/**
	 * @return the zxAlaramDetailLogList
	 */
	public List<ZxAlarmDetailLog> getZxAlaramDetailLogList() {
		return zxAlaramDetailLogList;
	}
	/**
	 * @param zxAlaramDetailLogList the zxAlaramDetailLogList to set
	 */
	public void setZxAlaramDetailLogList(
			List<ZxAlarmDetailLog> zxAlaramDetailLogList) {
		this.zxAlaramDetailLogList = zxAlaramDetailLogList;
	}
	/**
	 * @return the alarmSeq
	 */
	public String getAlarmSeq() {
		return alarmSeq;
	}
	/**
	 * @param alarmSeq the alarmSeq to set
	 */
	public void setAlarmSeq(String alarmSeq) {
		this.alarmSeq = alarmSeq;
	}
	/**
	 * @return the alarmTime
	 */
	public Timestamp getAlarmTime() {
		return alarmTime;
	}
	/**
	 * @param alarmTime the alarmTime to set
	 */
	public void setAlarmTime(Timestamp alarmTime) {
		this.alarmTime = alarmTime;
	}
	/**
	 * @return the alarmTypeId
	 */
	public String getAlarmTypeId() {
		return alarmTypeId;
	}
	/**
	 * @param alarmTypeId the alarmTypeId to set
	 */
	public void setAlarmTypeId(String alarmTypeId) {
		this.alarmTypeId = alarmTypeId;
	}
	/**
	 * @return the alarmLevel
	 */
	public String getAlarmLevel() {
		return alarmLevel;
	}
	/**
	 * @param alarmLevel the alarmLevel to set
	 */
	public void setAlarmLevel(String alarmLevel) {
		this.alarmLevel = alarmLevel;
	}
	/**
	 * @return the logType
	 */
	public String getLogType() {
		return logType;
	}
	/**
	 * @param logType the logType to set
	 */
	public void setLogType(String logType) {
		this.logType = logType;
	}
	/**
	 * @return the hostName
	 */
	public String getHostName() {
		return hostName;
	}
	/**
	 * @param hostName the hostName to set
	 */
	public void setHostName(String hostName) {
		this.hostName = hostName;
	}
	/**
	 * @return the recoverTime
	 */
	public Timestamp getRecoverTime() {
		return recoverTime;
	}
	/**
	 * @param recoverTime the recoverTime to set
	 */
	public void setRecoverTime(Timestamp recoverTime) {
		this.recoverTime = recoverTime;
	}
	/**
	 * @return the remark
	 */
	public String getRemark() {
		return remark;
	}
	/**
	 * @param remark the remark to set
	 */
	public void setRemark(String remark) {
		this.remark = remark;
	}
	

}
